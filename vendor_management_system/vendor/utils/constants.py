class PurchaseOrderStatus:
    pending = "pending"
    completed_on_time = "completed_on_time"
    completed = "completed"
    canceled = "canceled"

    success_status_list = [completed,completed_on_time]

    choices = (
        ("pending", "pending"),
        ("completed_on_time", "completed_on_time"),
        ("completed", "completed"),
        ("canceled", "canceled"),
    )
