import asyncio
from utils.pprint import pprint

''' Runner class to run consistency check in async and sync mode
    times = 3
'''
class Runner:
    async def async_consistency_check(self, foo):
        results = await asyncio.gather(foo(), foo(), foo())
        pprint(results)
        return results

    def consistency_check(self, foo):
        result1 = foo()
        result2 = foo()
        result3 = foo()
        pprint([result1, result2,result3])
        return [result1, result2, result3]
