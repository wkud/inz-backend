from inz.models.limit import Limit
from inz import db
from inz.exceptions.unauthorized_error import UnauthorizedError
from inz.exceptions.record_not_found_error import RecordNotFoundError
from inz.exceptions.invalid_duration_error import InvalidDurationError
from inz.utility.list_utility import contains
from inz.utility.duration_utility import duration_contains
from datetime import date


class LimitService:
    @staticmethod
    def create(duration_start_date_string, duration_end_date_string,
               planned_amount, category_id, current_user_categories):
        # validate access to category_id
        category_accessible = contains(current_user_categories,
                                       lambda c: c.id == category_id)
        if not category_accessible:
            raise UnauthorizedError(msg='Given category cannot be accessed')

        duration_start = date.fromisoformat(duration_start_date_string)
        duration_end = date.fromisoformat(duration_end_date_string)

        # validate date constraints
        if duration_start > duration_end:
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

    @ staticmethod
    def get_spent_amount(limit):
        expenses_from_category = limit.category.expenses
        expenses_from_duration = [e for e in expenses_from_category
                                  if duration_contains(
                                      limit.duration_start,
                                      limit.duration_end, e.date)]
        spent_amount = sum([e.price * e.amount
                            for e in expenses_from_duration])
        return spent_amount

    @staticmethod
    def get_info_of(limit):
        duration_length = (limit.duration_end - limit.duration_start).days + 1
        duration_past = (date.today() - limit.duration_start).days
        duration_past = min(duration_past, duration_length)
        duration_past = max(0, duration_past)

        planned_amount = limit.planned_amount
        spent_amount = LimitService.get_spent_amount(limit)

        saving_rate = 'bad' \
            if spent_amount/planned_amount > duration_past/duration_length \
            else 'good'

        return {'saving_rate': saving_rate,
                'spent_amount': spent_amount,
                'duration_past': duration_past,
                'duration_length': duration_length}
