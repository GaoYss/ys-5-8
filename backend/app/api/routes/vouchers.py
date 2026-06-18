from fastapi import APIRouter

from app.schemas.loyalty import RedeemVoucherRequest, Voucher
from app.services.loyalty_service import LoyaltyService

router = APIRouter()
service = LoyaltyService()


@router.get("", response_model=list[Voucher])
def list_vouchers() -> list[dict]:
    return service.list_vouchers()


@router.post("/birthday/issue", response_model=list[Voucher])
def issue_birthday_vouchers() -> list[dict]:
    return service.issue_birthday_vouchers()


@router.post("/redeem")
def redeem_voucher(request: RedeemVoucherRequest) -> dict:
    return service.redeem_voucher(request.voucher_id)


@router.post("/revert")
def revert_voucher(request: RedeemVoucherRequest) -> dict:
    return service.revert_voucher(request.voucher_id)
