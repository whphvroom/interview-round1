import torch


class KVCache:
    """
    A simple KV cache for autoregressive transformer inference.

    At each generation step, one new token is processed. Its key and value
    vectors are appended to the cache so that attention can be computed
    against the full history without recomputing past tokens.

    Internal buffers grow along the sequence dimension at each step:
        k_cache: (batch_size, seq_len_so_far, d_k)
        v_cache: (batch_size, seq_len_so_far, d_v)
    """

    def __init__(self):
        # TODO: Initialize k_cache and v_cache to None.
        #       They will be created on the first call to update().
        pass

    def update(self, new_k, new_v):
        """
        Append new key and value vectors to the cache.

        Args:
            new_k: Key for the current token, shape (batch_size, 1, d_k)
            new_v: Value for the current token, shape (batch_size, 1, d_v)

        After update, internal buffers should have shape:
            k_cache: (batch_size, seq_len_so_far + 1, d_k)
            v_cache: (batch_size, seq_len_so_far + 1, d_v)
        """
        # TODO: On the first call, initialize the buffers directly from new_k and new_v.
        #       On subsequent calls, concatenate new_k / new_v along the sequence dimension.
        pass

    def get(self):
        """
        Return the full cached keys and values.

        Returns:
            k_cache: (batch_size, seq_len_so_far, d_k)
            v_cache: (batch_size, seq_len_so_far, d_v)
        """
        # TODO: Return the current buffers.
        pass


def attention_with_cache(query, cache):
    """
    Compute attention for the current token query against the full cached context.

    Args:
        query: Query vector for the current token, shape (batch_size, 1, d_k)
        cache: A KVCache instance holding all past (and current) keys and values

    Returns:
        output: Attention output for the current token, shape (batch_size, 1, d_v)
    """
    d_k = query.size(-1)

    # TODO: Retrieve full keys and values from the cache.

    # TODO: Compute scaled dot-product attention scores between query and all cached keys.
    #       scores shape: (batch_size, 1, seq_len_so_far)

    # TODO: Apply softmax and compute the weighted sum over cached values.
    #       output shape: (batch_size, 1, d_v)

    pass


if __name__ == "__main__":
    batch_size = 1
    d_k = 8
    d_v = 16

    cache = KVCache()

    for step in range(5):
        # Simulate one new token at each step
        new_k = torch.randn(batch_size, 1, d_k)
        new_v = torch.randn(batch_size, 1, d_v)
        query = torch.randn(batch_size, 1, d_k)

        cache.update(new_k, new_v)
        output = attention_with_cache(query, cache)

        k_cache, _ = cache.get()
        print(f"Step {step + 1} | cache size: {k_cache.shape[1]} | output shape: {output.shape}")
        # Expected:
        # Step 1 | cache size: 1 | output shape: (1, 1, 16)
        # Step 2 | cache size: 2 | output shape: (1, 1, 16)
        # ...
