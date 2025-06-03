from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from chat.infrastructure.connections.connection_manager import ConnectionManager
from chat.api.dependencies import user_dependency
from infrastructure.db.dependencies import db_dependency
from chat.use_cases.messages_operations import GetPendingMessagesUseCase, SaveMessagesUseCase, GetChatHistory
from chat.infrastructure.repositories.message_repository_sql import MessageRepositorySQL, MessageHistoryRepositorySQL
from chat.entities.message_entity import MessageEntity
from auth.services.jwt_services import AccessTokenGenerator
from chat.schemas.message_schema import MessageSchema
from datetime import datetime, UTC
from utils.models import User, AppointmentModel

manager = ConnectionManager()

router = APIRouter(
    prefix="/chat",
    tags=["Chat server"]
)

@router.get("/history")
async def get_chat_history(receiver_id: int, db: db_dependency, user: dict = Depends(user_dependency)):
    sender_id = user["id"]
    sender_role = user["role"]

    # Fetch receiver role
    receiver_user = db.query(User).filter(User.user_id == receiver_id).first()
    if not receiver_user:
        raise HTTPException(status_code=404, detail="Receiver not found")

    receiver_role = receiver_user.role

    # Enforce same-role restrictions
    if sender_role == "patient" and receiver_role == "patient":
        raise HTTPException(status_code=403, detail="Patients cannot chat with other patients")
    if sender_role == "doctor" and receiver_role == "doctor":
        raise HTTPException(status_code=403, detail="Doctors cannot chat with other doctors")

    # If sender is patient → check appointment
    if sender_role == "patient":
        appointment = db.query(AppointmentModel).filter(
            AppointmentModel.user_id == sender_id,
            AppointmentModel.doctor_id == receiver_id,
            AppointmentModel.status == "accepted"
        ).first()
        if not appointment:
            raise HTTPException(status_code=403, detail="No accepted appointment with this doctor")

    # If sender is doctor → check reverse appointment
    if sender_role == "doctor":
        appointment = db.query(AppointmentModel).filter(
            AppointmentModel.user_id == receiver_id,
            AppointmentModel.doctor_id == sender_id,
            AppointmentModel.status == "accepted"
        ).first()
        if not appointment:
            raise HTTPException(status_code=403, detail="No accepted appointment with this patient")

    repo = MessageHistoryRepositorySQL(db)
    use_case = GetChatHistory(repo)
    return {"History": use_case.execute(sender_id=sender_id, receiver_id=receiver_id)}


@router.websocket("/ws/{receiver_id}")
async def websocket_endpoint(websocket: WebSocket, receiver_id: int, db: db_dependency, token: str):
    try:
        TokenGenerator = AccessTokenGenerator()
        decoded_token = TokenGenerator.decode(token)
        if decoded_token is None:
            await websocket.close(code=4001)
            return
    except Exception:
        await websocket.close(code=4001)
        return

    sender_id = decoded_token["id"]
    sender_role = decoded_token["role"]
    user_key = f"UserID:{sender_id}"

    # Check roles
    if sender_role not in ["patient", "doctor"]:
        await manager.send_personal_message("Invalid user role.", websocket)
        await websocket.close(code=4003)
        return

    # Fetch receiver role
    receiver_user = db.query(User).filter(User.user_id == receiver_id).first()
    if not receiver_user:
        await manager.send_personal_message("Receiver not found.", websocket)
        await websocket.close(code=4004)
        return

    receiver_role = receiver_user.role

    # Enforce messaging rules
    if sender_role == "patient" and receiver_role == "patient":
        await manager.send_personal_message("Patients cannot chat with other patients.", websocket)
        await websocket.close(code=4005)
        return
    if sender_role == "doctor" and receiver_role == "doctor":
        await manager.send_personal_message("Doctors cannot chat with other doctors.", websocket)
        await websocket.close(code=4006)
        return

    # If sender is patient → check appointment
    if sender_role == "patient":
        appointment = db.query(AppointmentModel).filter(
            AppointmentModel.user_id == sender_id,
            AppointmentModel.doctor_id == receiver_id,
            AppointmentModel.status == "accepted"
        ).first()
        if not appointment:
            await manager.send_personal_message(
                "You cannot send messages without an accepted appointment.", websocket
            )
            await websocket.close(code=4007)
            return

    # If sender is doctor → check reverse appointment
    if sender_role == "doctor":
        appointment = db.query(AppointmentModel).filter(
            AppointmentModel.user_id == receiver_id,
            AppointmentModel.doctor_id == sender_id,
            AppointmentModel.status == "accepted"
        ).first()
        if not appointment:
            await manager.send_personal_message(
                "You cannot send messages without an accepted appointment.", websocket
            )
            await websocket.close(code=4008)
            return

    repo = MessageRepositorySQL(db)
    pending_use_case = GetPendingMessagesUseCase(repo)
    save_use_case = SaveMessagesUseCase(repo)

    await manager.connect(user_key, websocket)

    response = pending_use_case.execute(sender_id=receiver_id, receiver_id=sender_id)
    if response:
        for i in response:
            formatted = f"{i.sender_id}:{i.content}"
            await manager.send_personal_message(formatted, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            recipient_str, message = data.split(':', 1)
            recipient_str = recipient_str.strip()
            message = message.strip()
            recipient_id = int(recipient_str)
            recipient_user_key = f"UserID:{recipient_id}"

            # Re-fetch receiver user
            receiver_user = db.query(User).filter(User.user_id == recipient_id).first()
            if not receiver_user:
                await manager.send_personal_message("Receiver not found.", websocket)
                continue

            receiver_role = receiver_user.role

            # Validate roles again (for each message sent)
            if sender_role == "patient" and receiver_role == "patient":
                await manager.send_personal_message("Patients cannot chat with other patients.", websocket)
                continue

            if sender_role == "doctor" and receiver_role == "doctor":
                await manager.send_personal_message("Doctors cannot chat with other doctors.", websocket)
                continue

            # Check appointment status (for each message sent)
            if sender_role == "patient":
                appointment = db.query(AppointmentModel).filter(
                    AppointmentModel.user_id == sender_id,
                    AppointmentModel.doctor_id == recipient_id,
                    AppointmentModel.status == "accepted"
                ).first()
                if not appointment:
                    await manager.send_personal_message(
                        "You cannot send messages without an accepted appointment.", websocket
                    )
                    continue

            if sender_role == "doctor":
                appointment = db.query(AppointmentModel).filter(
                    AppointmentModel.user_id == recipient_id,
                    AppointmentModel.doctor_id == sender_id,
                    AppointmentModel.status == "accepted"
                ).first()
                if not appointment:
                    await manager.send_personal_message(
                        "You cannot send messages without an accepted appointment.", websocket
                    )
                    continue

            # Try to deliver the message
            sent = await manager.send_message_to_user(recipient_user_key, f"{sender_id}:{message}")
            if not sent:
                pending_message = MessageEntity(MessageSchema(
                    sender_id=sender_id,
                    receiver_id=recipient_id,
                    content=message,
                    sent_at=datetime.now(UTC),
                    status='pending'
                ))
                save_use_case.execute(pending_message)

            # Save the message as sent
            save_use_case.execute(MessageEntity(MessageSchema(
                sender_id=sender_id,
                receiver_id=recipient_id,
                content=message,
                sent_at=datetime.now(UTC),
                delivered_at=datetime.now(UTC),
                status='sent'
            )))

    except WebSocketDisconnect:
        manager.disconnect(user_key)