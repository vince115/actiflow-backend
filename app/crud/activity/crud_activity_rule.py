# app/crud/activity/crud_activity_rule.py

from sqlalchemy.orm import Session
from app.crud.base.crud_base import CRUDBase
from app.models.activity.activity_rule import ActivityRule

from app.schemas.activity_rule.activity_rule_create import ActivityRuleCreate
from app.schemas.activity_rule.activity_rule_update import ActivityRuleUpdate


class CRUDActivityRule(CRUDBase[ActivityRule]):

    def create(self, db: Session, data: ActivityRuleCreate) -> ActivityRule:
        return super().create(db, obj_in=data.model_dump())

    def update(
        self,
        db: Session,
        db_obj: ActivityRule,
        data: ActivityRuleUpdate
    ) -> ActivityRule:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )


activity_rule_crud = CRUDActivityRule(ActivityRule)
