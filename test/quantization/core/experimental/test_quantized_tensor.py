# Owner(s): ["oncall: quantization"]

import torch
from torch.ao.quantization.experimental.APoT_tensor import TensorAPoT
from torch.ao.quantization.experimental.observer import APoTObserver
import unittest

class TestQuantizedTensor(unittest.TestCase):
    def test_quantize_APoT(self):
        t = TensorAPoT()

        tensor2quantize = torch.tensor([0.343, 0.0419, 0.1663, 1])

        result = t.quantize_APoT(tensor2quantize, 4, 2)

        print(result)

        max_val = torch.max(tensor2quantize)

        # make observer
        obs = APoTObserver(max_val=max_val, b=4, k=2)
        obs_result = obs.calculate_qparams(signed=False)

        quantized_levels = obs_result[1]
        level_indices = obs_result[2]

        tensor2quantize_arr = list(tensor2quantize)
        result_arr = result.numpy()

        zipped_result = zip(tensor2quantize_arr, result_arr)

        expected_result = True

        for ele, res in zipped_result:
            idx = list(level_indices).index(ele)
            if res != quantized_levels[idx]:
                expected_result = False

        self.assertTrue(expected_result)

    def test_dequantize(self):
        with self.assertRaises(NotImplementedError):
            TensorAPoT.dequantize(self)

    def test_q_apot_alpha(self):
        with self.assertRaises(NotImplementedError):
            TensorAPoT.q_apot_alpha(self)

if __name__ == '__main__':
    unittest.main()
