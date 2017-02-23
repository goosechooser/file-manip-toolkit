import sys
from struct import Struct, error

def deinterleave(data, nbytes, nsplit):
    """Deinterleaves one bytearray into nsplit many bytearrays on a nbytes basis.

    Returns a list of bytearrays.
    """
    deinterleaved = [[] for n in range(nsplit)]

    deinterleave_s = Struct('c' * nbytes)

    try:
        deinterleave_iter = deinterleave_s.iter_unpack(data)
    except error as err:
        #this error can be many things, handling generically until otherwise
        print('ERROR:', err, 'CLOSING', file=sys.stderr)
        raise err

    #this could cause rounding errors?
    iterlen = int(len(data) / (nbytes * nsplit))
    for _ in range(iterlen):
        for i, _ in enumerate(deinterleaved):
            try:
                next_ = next(deinterleave_iter)
            except StopIteration:
                pass
            deinterleaved[i].extend([*next_])

    return [b''.join(delist) for delist in deinterleaved]

def interleave(data, nbytes):
    """Interleaves a list of bytearrays together on a nbytes basis.

    Returns a bytearray.
    """
    interleave_s = Struct('c' * nbytes)
    iters = []

    for inter in data:
        try:
            iters.append(interleave_s.iter_unpack(inter))
        except error as err:
            print('ERROR:', err, 'CLOSING', file=sys.stderr)
            raise err

    interleaved = []
    #this could cause rounding errors?
    iterlen = int(len(data[0]) / nbytes)
    for _ in range(iterlen):
        nexts = [next(iter_) for iter_ in iters]
        interleaved.extend([b''.join(val) for val in nexts])

    return b''.join(interleaved)
    