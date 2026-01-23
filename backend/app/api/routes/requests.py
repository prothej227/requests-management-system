from fastapi import APIRouter, Depends, HTTPException, Response, Body, status
import app.schemas.request as record_schemas
from app.schemas.generic import APIResponse
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.request_service import RequestService, CustomerService, AreaService

router = APIRouter(
    prefix="/records",
    tags=["records"],
)


@router.post("/requests/create", status_code=status.HTTP_200_OK)
async def create_request(
    form_data: record_schemas.RequestCreateSchema,
    db: AsyncSession = Depends(get_db),
) -> APIResponse:
    """
    Create a new request record.

    Args:
        db (AsyncSession): The database session.

    Returns:
        APIResponse: The created request object.
    """
    try:
        request_service = RequestService(db)
        created_data = await request_service.create(form_data)  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not created_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Request creation failed"
        )
    return APIResponse(
        response={"new_request_id": created_data.id},
        message="Request created successfully",
    )


@router.patch("/requests/update/{request_id}", status_code=status.HTTP_200_OK)
async def update_request(
    update_data: record_schemas.RequestUpdateSchema, request_id: int, db=Depends(get_db)
) -> APIResponse:
    """
    Update an existing request record.

    Args:
        db (AsyncSession): The database session.
        request_id (int): The ID of the request to update.
        update_data (RequestUpdateSchema): The data to update the request with.

    Returns:
        APIResponse: The updated request object.
    """
    try:
        request_service = RequestService(db)
        updated_record = await request_service.update(request_id, update_data)  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not updated_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Request update failed"
        )
    return APIResponse(
        response={"updated_request_id": updated_record.id},
        message="Request updated successfully",
    )


@router.get("/requests/get/{request_id}", status_code=status.HTTP_200_OK)
async def get_request(
    request_id: int,
    db: AsyncSession = Depends(get_db),
) -> record_schemas.RequestViewSchema:
    """
    Get a request by ID.

    Args:
        db (AsyncSession): The database session.
        request_id (int): The ID of the request to retrieve.

    Returns:
        APIResponse: The retrieved request object.
    """
    try:
        request_service = RequestService(db)
        record = await request_service.get_by_id(
            request_id, relationships=["customer", "area"]
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Request not found"
        )
    # Build dict of model columns
    data = {c.name: getattr(record, c.name) for c in record.__table__.columns}
    # Add relationships if present
    if hasattr(record, "customer"):
        data["customer_name"] = getattr(record.customer, "name", None)
    if hasattr(record, "area"):
        data["area_name"] = getattr(record.area, "name", None)
    return record_schemas.RequestViewSchema.model_validate(data)


@router.get("/requests/list", status_code=status.HTTP_200_OK)
async def list_requests(
    db: AsyncSession = Depends(get_db), start_index: int = 0, batch_size: int = 30
) -> record_schemas.RequestResponseWithCount:
    """
    List all requests.

    Args:
        db (AsyncSession): The database session.

    Returns:
        APIResponse: A list of request objects.
    """
    record_list = []
    try:
        request_service = RequestService(db)
        records = await request_service.get_all_denorm_with_count(
            start_index=start_index,
            batch_size=batch_size,
            relationships=["customer", "area"],
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    for record in records["records"]:
        data = {c.name: getattr(record, c.name) for c in record.__table__.columns}
        if hasattr(record, "customer"):
            data["customer_name"] = getattr(record.customer, "name", "-")
        if hasattr(record, "area"):
            data["area_name"] = getattr(record.area, "name", "-")
        record_list.append(data)
    return record_schemas.RequestResponseWithCount(
        total_count=records["total_count"],
        records=[
            record_schemas.RequestViewSchema.model_validate(record)
            for record in record_list
        ],
    )


@router.post("/customers/create", status_code=status.HTTP_200_OK)
async def create_customer(
    form_data: record_schemas.CustomerCreateSchema,
    db=Depends(get_db),
) -> APIResponse:
    """
    Create a new customer record.

    Args:
        db (AsyncSession): The database session.

    Returns:
        APIResponse: The created customer object.
    """
    try:
        customer_service = CustomerService(db)
        created_data = await customer_service.create(form_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not created_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Customer creation failed"
        )
    return APIResponse(
        response={"new_customer_id": created_data.id},
        message="Customer created successfully",
    )


@router.patch("/customers/update/{customer_id}", status_code=status.HTTP_200_OK)
async def update_customer(
    customer_id: int,
    update_data: record_schemas.CustomerUpdateSchema,
    db=Depends(get_db),
) -> APIResponse:
    """
    Update an existing customer record.

    Args:
        db (AsyncSession): The database session.
        customer_id (int): The ID of the customer to update.
        update_data (CustomerUpdateSchema): The data to update the customer with.

    Returns:
        APIResponse: The updated customer object.
    """
    try:
        customer_service = CustomerService(db)
        updated_record = await customer_service.update(customer_id, update_data)  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not updated_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Customer update failed"
        )
    return APIResponse(
        response={"updated_customer_id": updated_record.id},
        message="Customer updated successfully",
    )


@router.post("/areas/create", status_code=status.HTTP_200_OK)
async def create_area(
    form_data: record_schemas.AreaCreateSchema, db: AsyncSession = Depends(get_db)
) -> APIResponse:
    """
    Create a new area record.

    Args:
        db (AsyncSession): The database session.

    Returns:
        APIResponse: The created area object.
    """
    try:
        area_service = AreaService(db)
        created_data = await area_service.create(form_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not created_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Area creation failed"
        )
    return APIResponse(
        response={"new_area_id": created_data.id},
        message="Area created successfully",
    )


@router.patch("/areas/update/{area_id}", status_code=status.HTTP_200_OK)
async def update_area(
    area_id: int, db=Depends(get_db), update_data=record_schemas.AreaUpdateSchema
) -> APIResponse:
    """
    Update an existing area record.

    Args:
        db (AsyncSession): The database session.
        area_id (int): The ID of the area to update.
        update_data (AreaUpdateSchema): The data to update the area with.

    Returns:
        APIResponse: The updated area object.
    """
    try:
        area_service = AreaService(db)
        updated_record = await area_service.update(area_id, update_data)  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not updated_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Area update failed"
        )
    return APIResponse(
        response={"updated_area_id": updated_record.id},
        message="Area updated successfully",
    )
