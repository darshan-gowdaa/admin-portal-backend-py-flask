from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from ..models import db, Opportunity, VALID_CATEGORIES

opp_bp = Blueprint('opportunities', __name__)


def opp_to_dict(opp):
    return {
        'id':                   opp.id,
        'admin_id':             opp.admin_id,
        'name':                 opp.name,
        'category':             opp.category,
        'duration':             opp.duration,
        'start_date':           opp.start_date,
        'description':          opp.description,
        'skills_to_gain':       opp.skills_to_gain,
        'future_opportunities': opp.future_opportunities,
        'max_applicants':       opp.max_applicants,
        'created_at':           opp.created_at.isoformat() if opp.created_at else None,
    }


def _validate(data):
    """Returns (cleaned_dict, error_string). error_string is None on success."""
    required = ['name', 'category', 'duration', 'start_date', 'description',
                'skills_to_gain', 'future_opportunities']
    cleaned = {}

    for field in required:
        val = (data.get(field) or '').strip()
        if not val:
            return None, f'Field "{field}" is required.'
        cleaned[field] = val

    if cleaned['category'] not in VALID_CATEGORIES:
        return None, f'Invalid category. Must be one of: {", ".join(sorted(VALID_CATEGORIES))}.'

    raw_max = str(data.get('max_applicants') or '').strip()
    if raw_max:
        try:
            max_val = int(raw_max)
            if max_val <= 0:
                raise ValueError
            cleaned['max_applicants'] = max_val
        except ValueError:
            return None, 'max_applicants must be a positive integer.'
    else:
        cleaned['max_applicants'] = None

    return cleaned, None


# GET /api/opportunities/
@opp_bp.route('/', methods=['GET'])
@login_required
def get_opportunities():
    opps = (Opportunity.query
            .filter_by(admin_id=current_user.id)
            .order_by(Opportunity.created_at.desc())
            .all())
    return jsonify([opp_to_dict(o) for o in opps]), 200


# POST /api/opportunities/
@opp_bp.route('/', methods=['POST'])
@login_required
def create_opportunity():
    data = request.get_json(silent=True) or request.form
    cleaned, err = _validate(data)
    if err:
        return jsonify({'error': err}), 400

    opp = Opportunity(admin_id=current_user.id, **cleaned)
    db.session.add(opp)
    db.session.commit()
    return jsonify(opp_to_dict(opp)), 201


# GET /api/opportunities/<id>
@opp_bp.route('/<int:opp_id>', methods=['GET'])
@login_required
def get_opportunity(opp_id):
    opp = Opportunity.query.get_or_404(opp_id)
    if opp.admin_id != current_user.id:
        return jsonify({'error': 'Forbidden.'}), 403
    return jsonify(opp_to_dict(opp)), 200


# PUT /api/opportunities/<id>
@opp_bp.route('/<int:opp_id>', methods=['PUT'])
@login_required
def update_opportunity(opp_id):
    opp = Opportunity.query.get_or_404(opp_id)
    if opp.admin_id != current_user.id:
        return jsonify({'error': 'Forbidden.'}), 403

    data = request.get_json(silent=True) or request.form
    cleaned, err = _validate(data)
    if err:
        return jsonify({'error': err}), 400

    for key, val in cleaned.items():
        setattr(opp, key, val)
    db.session.commit()
    return jsonify(opp_to_dict(opp)), 200


# DELETE /api/opportunities/<id>
@opp_bp.route('/<int:opp_id>', methods=['DELETE'])
@login_required
def delete_opportunity(opp_id):
    opp = Opportunity.query.get_or_404(opp_id)
    if opp.admin_id != current_user.id:
        return jsonify({'error': 'Forbidden.'}), 403

    db.session.delete(opp)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully.'}), 200
