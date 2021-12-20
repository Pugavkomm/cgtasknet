from typing import Optional, Tuple

import norse.torch as snn
import torch
from norse.torch.functional.lsnn import LSNNParameters, LSNNState
from norse.torch.module.exp_filter import ExpFilter

default_tau_filter_inv = 223.1435511314


class SNNAlif(torch.nn.Module):
    r"""This net includes one adaptive integrate-and-fire layer."""

    def __init__(
        self,
        feature_size,
        hidden_size,
        output_size,
        neuron_parameters: Optional[LSNNParameters] = None,
        tau_filter_inv: float = default_tau_filter_inv,
    ) -> None:
        super(SNNAlif, self).__init__()
        self.lif = snn.LIFRecurrent(feature_size, int(hidden_size * 0.6))
        if neuron_parameters is not None:
            self.alif = snn.LSNNRecurrent(
                int(hidden_size * 0.6), hidden_size, p=neuron_parameters
            )
        else:
            self.alif = snn.LSNNRecurrent(
                int(hidden_size * 0.6), int(hidden_size * 0.4)
            )
        self.exp_f = ExpFilter(int(hidden_size * 0.4), output_size, tau_filter_inv)

    def forward(self, x: torch.tensor) -> Tuple[torch.tensor, LSNNState]:
        out = self.lif(x)[0]
        out, state = self.alif(out)
        out = self.exp_f(out)
        return (out, state)

    @staticmethod
    def type_parameters():
        return LSNNParameters

    @staticmethod
    def type_state():
        return LSNNState