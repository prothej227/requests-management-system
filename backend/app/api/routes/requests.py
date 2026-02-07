from fastapi import APIRouter, Depends, HTTPException, status
import app.schemas.request as record_schemas
from app.models.stickers import Sticker, StickerCanvas
from app.schemas.generic import APIResponse
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import Union, Optional
from app.services.request_service import (
    RequestService,
    CustomerService,
    AreaService,
    SalesPersonService,
)

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
    is_normal: bool = True,
    db: AsyncSession = Depends(get_db),
) -> Union[record_schemas.RequestViewSchema, record_schemas.RequestNormalViewSchema]:
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
            request_id, relationships=["customer", "area", "sales_person"]
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Request not found"
        )

    if is_normal:
        return record_schemas.RequestNormalViewSchema.model_validate(record)

    # Build dict of model columns
    data = {c.name: getattr(record, c.name) for c in record.__table__.columns}
    # Add relationships if present
    if hasattr(record, "customer"):
        data["customer_name"] = getattr(record.customer, "name", None)
    if hasattr(record, "area"):
        data["area_name"] = getattr(record.area, "name", None)
    if hasattr(record, "sales_person"):
        data["sales_person"] = (
            f"{getattr(record.sales_person, "first_name", "")} {getattr(record.sales_person, "last_name", "")}"
        )
    return record_schemas.RequestViewSchema.model_validate(data)


@router.delete("/requests/delete/{request_id}", status_code=status.HTTP_200_OK)
async def delete_request(
    request_id: int, db: AsyncSession = Depends(get_db)
) -> APIResponse:
    service = RequestService(db)
    try:
        op = await service.delete_by_id(request_id)
        if not op:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Record with {request_id} cannot be found.",
            )
        return APIResponse(response={}, message="Delete OK.")
    except IntegrityError as e:
        await db.rollback()

        # Find sticker canvases still referencing this request
        stmt = (
            select(StickerCanvas.id)
            .join(Sticker)
            .where(Sticker.request_id == request_id)
            .distinct()
        )

        result = await db.execute(stmt)
        sticker_canvas_ids = result.scalars().all()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Request is used by the ff. sticker canvas: {sticker_canvas_ids}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )


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
            relationships=["customer", "area", "sales_person"],
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    for record in records["records"]:
        data = {c.name: getattr(record, c.name) for c in record.__table__.columns}
        if hasattr(record, "customer"):
            data["customer_name"] = getattr(record.customer, "name", "-")
        if hasattr(record, "area"):
            data["area_name"] = getattr(record.area, "name", "-")
        if hasattr(record, "sales_person"):
            if not record.sales_person:
                data["sales_person"] = "-"
            else:
                first_name = getattr(record.sales_person, "first_name", "-")
                last_name = getattr(record.sales_person, "last_name", "-")
                data["sales_person"] = f"{first_name} {last_name[0]}"
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


@router.get("/customers/list", status_code=status.HTTP_200_OK)
async def list_customers(
    db: AsyncSession = Depends(get_db), start_index: int = 0, batch_size: int = 30
) -> record_schemas.RequestResponseWithCount:
    """
    List all customers.

    Args:
        db (AsyncSession): The database session.

    Returns:
        APIResponse: A list of customer objects.
    """
    record_list = []
    try:
        customer_service = CustomerService(db)
        records = await customer_service.get_all_denorm_with_count(
            start_index=start_index,
            batch_size=batch_size,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    for record in records["records"]:
        data = {c.name: getattr(record, c.name) for c in record.__table__.columns}
        record_list.append(data)
    return record_schemas.RequestResponseWithCount(
        total_count=records["total_count"],
        records=[
            record_schemas.CustomerViewSchema.model_validate(record)
            for record in record_list
        ],
    )


@router.delete("/customers/delete/{customer_id}", status_code=status.HTTP_200_OK)
async def delete_customer(
    customer_id: int, db: AsyncSession = Depends(get_db)
) -> APIResponse:
    service = CustomerService(db)
    try:
        op = await service.delete_by_id(customer_id)
        if not op:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Record with {customer_id} cannot be found.",
            )
        return APIResponse(response={}, message="Delete OK.")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
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
        if form_data.logo:
            form_data.logo = area_service.decode_base64_image(form_data.logo)
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


@router.get("/areas/list", status_code=status.HTTP_200_OK)
async def list_areas(
    db: AsyncSession = Depends(get_db), start_index: int = 0, batch_size: int = 30
) -> record_schemas.RequestResponseWithCount:
    """
    List all areas.

    Args:
        db (AsyncSession): The database session.

    Returns:
        APIResponse: A list of area objects.
    """
    record_list = []
    try:
        area_service = AreaService(db)
        records = await area_service.get_all_denorm_with_count(
            start_index=start_index,
            batch_size=batch_size,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    for record in records["records"]:
        data = {}
        for column in record.__table__.columns:
            value = getattr(record, column.name)

            if isinstance(value, (bytes, bytearray)):
                value = area_service.bytes_to_base64(value)
            elif value == b"":  # optional safety
                value = None
            data[column.name] = value
        record_list.append(data)
    return record_schemas.RequestResponseWithCount(
        total_count=records["total_count"],
        records=[
            record_schemas.AreaViewSchema.model_validate(record)
            for record in record_list
        ],
    )


@router.delete("/areas/delete/{area_id}", status_code=status.HTTP_200_OK)
async def delete_area(area_id: int, db: AsyncSession = Depends(get_db)) -> APIResponse:
    service = AreaService(db)
    try:
        op = await service.delete_by_id(area_id)
        if not op:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Record with {area_id} cannot be found.",
            )
        return APIResponse(response={}, message="Delete OK.")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )


@router.post("/sales-persons/create", status_code=status.HTTP_200_OK)
async def create_sales_person(
    form_data: record_schemas.SalesPersonCreateSchema,
    db=Depends(get_db),
) -> APIResponse:
    """
    Create a new sales person record.

    Args:
        db (AsyncSession): The database session.

    Returns:
        APIResponse: The created sales person object.
    """
    try:
        sales_person_service = SalesPersonService(db)
        created_data = await sales_person_service.create(form_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not created_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sales Person creation failed",
        )
    return APIResponse(
        response={"new_sales_person_id": created_data.id},
        message="Sales Person created successfully",
    )


@router.patch("/sales-persons/update/{sales_person_id}", status_code=status.HTTP_200_OK)
async def update_sales_person(
    sales_person_id: int,
    update_data: record_schemas.SalesPersonUpdateSchema,
    db=Depends(get_db),
) -> APIResponse:
    """
    Update an existing sales person record.

    Args:
        db (AsyncSession): The database session.
        sales_person_id (int): The ID of the sales person to update.
        update_data (SalesPersonUpdateSchema): The data to update the sales person with.

    Returns:
        APIResponse: The updated sales person object.
    """
    try:
        sales_person_service = SalesPersonService(db)
        updated_record = await sales_person_service.update(sales_person_id, update_data)  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not updated_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Sales Person update failed"
        )
    return APIResponse(
        response={"updated_sales_person_id": updated_record.id},
        message="Sales Person updated successfully",
    )


@router.get("/sales-persons/list", status_code=status.HTTP_200_OK)
async def list_sales_persons(
    db: AsyncSession = Depends(get_db), start_index: int = 0, batch_size: int = 30
) -> record_schemas.RequestResponseWithCount:
    """
    List all sales persons.

    Args:
        db (AsyncSession): The database session.

    Returns:
        APIResponse: A list of sales person objects.
    """
    record_list = []
    try:
        sales_person_service = SalesPersonService(db)
        records = await sales_person_service.get_all_denorm_with_count(
            start_index=start_index,
            batch_size=batch_size,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    for record in records["records"]:
        data = {c.name: getattr(record, c.name) for c in record.__table__.columns}
        record_list.append(data)
    return record_schemas.RequestResponseWithCount(
        total_count=records["total_count"],
        records=[
            record_schemas.SalesPersonViewSchema.model_validate(record)
            for record in record_list
        ],
    )


@router.delete(
    "/sales-persons/delete/{sales_person_id}", status_code=status.HTTP_200_OK
)
async def delete_sales_person(
    sales_person_id: int, db: AsyncSession = Depends(get_db)
) -> APIResponse:
    service = SalesPersonService(db)
    try:
        op = await service.delete_by_id(sales_person_id)
        if not op:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Record with {sales_person_id} cannot be found.",
            )
        return APIResponse(response={}, message="Delete OK.")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )
