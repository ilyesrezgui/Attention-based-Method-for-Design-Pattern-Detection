# coding=utf-8
# Copyright 2023 Salesforce authors, The EleutherAI, and HuggingFace Teams. All rights reserved.
""" PyTorch CodeT5+ mbedding models.
The implementation is based on transformers.models.t5.modeling_t5 by adding a projection layer on T5EncoderModel
"""
from typing import Optional, Tuple, Union
import torch
from torch import nn
import torch.nn.functional as F
from transformers import T5EncoderModel
from transformers.modeling_outputs import (
    BaseModelOutput,
)
from .configuration_codet5p_embedding import CodeT5pEmbeddingConfig


class CodeT5pEmbeddingModel(T5EncoderModel):
    config_class = CodeT5pEmbeddingConfig

    authorized_missing_keys = [
        r"encoder.embed_tokens.weight",
    ]

    def __init__(self, config: CodeT5pEmbeddingConfig):
        super().__init__(config)
        self.proj = nn.Linear(config.d_model, config.embed_dim)

    def forward(
            self,
            input_ids: Optional[torch.LongTensor] = None,
            attention_mask: Optional[torch.FloatTensor] = None,
            head_mask: Optional[torch.FloatTensor] = None,
            inputs_embeds: Optional[torch.FloatTensor] = None,
            output_attentions: Optional[bool] = None,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
    ) -> Union[Tuple[torch.FloatTensor], BaseModelOutput]:
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        encoder_outputs = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
            inputs_embeds=inputs_embeds,
            head_mask=head_mask,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        embedding = F.normalize(self.proj(encoder_outputs.last_hidden_state[:, 0, :]), dim=-1)

        return embedding
