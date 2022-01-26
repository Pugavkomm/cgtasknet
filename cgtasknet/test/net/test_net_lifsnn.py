from cgtasknet.net.liflsnn import SNNAlif
import torch
from norse.torch.functional.lsnn import LSNNParameters, LSNNState


def test_init_lif_refrac():
    input_s, hidden_s, output_s = 100, 100, 100
    SNNAlif(input_s, hidden_s, output_s)


def test_set_custom_params_lif_refrac():
    input_s, hidden_s, output_s = 100, 100, 100
    p = LSNNParameters()
    SNNAlif(input_s, hidden_s, output_s, neuron_parameters=p)


def test_run_lif_refrac():
    input_s, hidden_s, output_s = 100, 100, 10
    batch_size = 100
    data = torch.zeros((1000, batch_size, input_s))
    model = SNNAlif(input_s, hidden_s, output_s)
    outputs, state = model(data)
    assert outputs.shape == (1000, batch_size, output_s)
    assert type(state) == LSNNState


def test_run_save_state_lif_refrac():
    input_s, hidden_s, output_s = 100, 100, 10
    batch_size = 100
    data = torch.zeros((10, batch_size, input_s))
    model = SNNAlif(input_s, hidden_s, output_s, save_states=True)
    outputs, state = model(data)
    assert outputs.shape == (10, batch_size, output_s)
    assert len(state) == 10
    for i in range(10):
        assert type(state[i]) == LSNNState
