from inz.models.limit import Limit
from inz import db
from inz.exceptions.unauthorized_error import UnauthorizedError
from inz.exceptions.record_not_found_error import RecordNotFoundError
from inz.exceptions.invalid_duration_error import InvalidDurationError
from inz.utility.list_utility import contains
from datetime import date


class LimitService:
    @staticmethod
    def create(duration_start_date_string, duration_end_date_string,
               planned_amount, category_id, current_user_categories):
        # validate access
        is_accessible = contains(current_user_categories,
                                 lambda c: c.id == category_id)
        if not is_accessible:
            raise UnauthorizedError(msg='Given category cannot be accessed')

        duration_start = date.fromisoformat(duration_start_date_string)
        duration_end = date.fromisoformat(duration_end_date_string)

        # validate date constraints
        if duration_start >= duration_end:
            raise InvalidDurationError()

        new_limit = Limit(duration_start=duration_start,
                          duration_end=duration_end,
                          planned_amount=planned_amount,
                          category_id=category_id)
        db.session.add(new_limit)
        db.session.commit()
        return new_limit

    @staticmethod
    def update(limit_id, current_user_id, duration_start_date_string,
               duration_end_date_string, planned_amount, category_id):
        # validate access
        limit = LimitService.get_by_id(limit_id, current_user_id)

        new_data = dict(duration_start=duration_start_date_string,
                        duration_end=duration_end_date_string,
                        planned_amount=planned_amount,
                        category_id=category_id)
        for field in new_data.copy():
            if new_data[field] is None:
                del new_data[field]

        if len(new_data) == 0:
            return

        # if date_strings != None: convert to date objects
        if 'duration_start' in new_data:
            new_data['duration_start'] = date.fromisoformat(
                duration_start_date_string)
        if 'duration_end' in new_data:
            new_data['duration_end'] = date.fromisoformat(
                duration_end_date_string)

        # validate date constraints
        if 'duration_start' in new_data and 'duration_end' in new_data:
            # both has changed => start must be < than end
            if new_data['duration_start'] >= new_data['duration_end']:
                raise InvalidDurationError()
        elif 'duration_start' in new_data:
            # new start must be < than old end
            if new_data['duration_start'] >= limit.duration_end:
                raise InvalidDurationError()
        elif 'duration_end' in new_data:
            # old start must be < than new end
            if limit.duration_start >= new_data['duration_end']:
                raise InvalidDurationError()

        Limit.query.filter_by(id=limit_id).update(new_data)
        db.session.commit()

    @ staticmethod
    def delete(limit_id, current_user_id):
        limit = LimitService.get_by_id(limit_id, current_user_id)
        db.session.delete(limit)
        db.session.commit()

    @ staticmethod
    def get_by_id(limit_id, current_user_id):
        limit = Limit.query.get(limit_id)
        if limit is None:
            raise RecordNotFoundError()
        if limit.category.user_id != current_user_id:
            raise UnauthorizedError()
        return limit
