class GetterUnion:
    def __init__(self, *getters):
        self._getters = getters

    async def __call__(self, **kwargs):
        result = {}

        for getter in self._getters:
            result.update(await getter(**kwargs))

        return result
