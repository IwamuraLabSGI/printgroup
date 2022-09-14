import math
import llah


# TODO: imgはnp.ndarrayで受け取るようにする
class FeatureCalculator:
    EFFECTIVE_DECIMAL_DIGIT = 2

    @classmethod
    def calc(cls, descriptors: llah.Descriptors):
        features: list[float] = []
        for descriptor in descriptors:
            features.extend(FeatureCalculator.__calc_from_descriptor(descriptor))
        return features

    @classmethod
    def __calc_from_descriptor(cls, descriptor: llah.Descriptor):
        features: list[int] = []
        for attrs in descriptor.multi_pattern_attributes:
            feature_elements: list[int] = []
            for attr in attrs:
                feature_elements.append(cls.__discretize(attr.perimeter_rate, 3))
                feature_elements.append(cls.__discretize(attr.area_rate, 2))

            feature = 0
            for i, elem in enumerate(feature_elements):
                feature += elem * ((10 ** cls.EFFECTIVE_DECIMAL_DIGIT) ** i)
            features.append(feature)

        return features

    @classmethod
    def __discretize(cls, val: float, multiple: int):
        if val > 1:
            val = 1 / val
        result = math.floor(val * (10 ** cls.EFFECTIVE_DECIMAL_DIGIT))
        result = math.floor(result / multiple) * multiple
        return result


