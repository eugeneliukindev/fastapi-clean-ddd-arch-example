from uuid import UUID

from fastapi import APIRouter, status

from src.application.services.account import AccountServiceDep
from src.presentation.schemas.accounts import AccountCreate, AccountResponse, MoneyRequest
from src.presentation.schemas.common.response import ApiResponse

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/{id}")
async def get_account(id: UUID, service: AccountServiceDep) -> ApiResponse[AccountResponse]:
    return ApiResponse(data=await service.get(id))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_account(data: AccountCreate, service: AccountServiceDep) -> ApiResponse[AccountResponse]:
    account = await service.create(
        owner=data.owner,
        initial_balance=data.initial_balance,
        currency=data.currency,
    )
    return ApiResponse(data=account)


@router.post("/{id}/deposit")
async def deposit(id: UUID, data: MoneyRequest, service: AccountServiceDep) -> ApiResponse[AccountResponse]:
    return ApiResponse(data=await service.deposit(id, data.amount, data.currency))


@router.post("/{id}/withdraw")
async def withdraw(id: UUID, data: MoneyRequest, service: AccountServiceDep) -> ApiResponse[AccountResponse]:
    return ApiResponse(data=await service.withdraw(id, data.amount, data.currency))


@router.post("/{id}/freeze")
async def freeze(id: UUID, service: AccountServiceDep) -> ApiResponse[AccountResponse]:
    return ApiResponse(data=await service.freeze(id))


@router.post("/{id}/unfreeze")
async def unfreeze(id: UUID, service: AccountServiceDep) -> ApiResponse[AccountResponse]:
    return ApiResponse(data=await service.unfreeze(id))


@router.delete("/{id}")
async def delete_account(id: UUID, service: AccountServiceDep) -> ApiResponse[AccountResponse]:
    return ApiResponse(data=await service.delete(id))
