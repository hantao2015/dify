# -*- coding:utf-8 -*-
from flask_restful import marshal_with, fields

from controllers.web import api
from controllers.web.wraps import WebApiResource

from core.llm.llm_builder import LLMBuilder
from models.provider import ProviderName
from models.model import App


class AppParameterApi(WebApiResource):
    """Resource for app variables."""
    variable_fields = {
        'key': fields.String,
        'name': fields.String,
        'description': fields.String,
        'type': fields.String,
        'default': fields.String,
        'max_length': fields.Integer,
        'options': fields.List(fields.String)
    }

    parameters_fields = {
        'opening_statement': fields.String,
        'suggested_questions': fields.Raw,
        'suggested_questions_after_answer': fields.Raw,
        'speech_to_text': fields.Raw,
        'more_like_this': fields.Raw,
        'user_input_form': fields.Raw,
    }

    @marshal_with(parameters_fields)
    def get(self, app_model: App, end_user):
        """Retrieve app parameters."""
        app_model_config = app_model.app_model_config
        provider_name = LLMBuilder.get_default_provider(app_model.tenant_id, 'whisper-1')

        return {
            'opening_statement': app_model_config.opening_statement,
            'suggested_questions': app_model_config.suggested_questions_list,
            'suggested_questions_after_answer': app_model_config.suggested_questions_after_answer_dict,
            'speech_to_text': app_model_config.speech_to_text_dict if provider_name == ProviderName.OPENAI.value else { 'enabled': False },
            'more_like_this': app_model_config.more_like_this_dict,
            'user_input_form': app_model_config.user_input_form_list
        }


api.add_resource(AppParameterApi, '/parameters')
