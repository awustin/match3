from model.effects.alignmentSparkles import AlignmentSparkles
from model.effects.aligmentPowerRatio import AligmentPowerRatio


class VisualEffects():
    def __init__(self):
        self.__effects = []

    def run_sparkles_alignment(self, origins):
        effect = AlignmentSparkles()
        effect.generate_particles(origins)
        effect.run_particles()
        self.__effects.append(effect)

    def run_power_ratio(self, origins):
        effect = AligmentPowerRatio()
        effect.run_power_ratio(origins)
        self.__effects.append(effect)

    def update_effects_sparkles_alignment(self, display):
        for effect in self.__effects:
            effect.update(display)
            if effect.has_ended():
                self.__effects.remove(effect)
