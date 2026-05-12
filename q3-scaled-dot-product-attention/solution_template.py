import torch
import torch.nn.functional as F


def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Compute scaled dot-product attention.

    Args:
        Q: Query matrix of shape (batch_size, seq_len_q, d_k)
        K: Key matrix of shape (batch_size, seq_len_k, d_k)
        V: Value matrix of shape (batch_size, seq_len_k, d_v)
        mask: Optional boolean mask of shape (batch_size, seq_len_q, seq_len_k).
              Positions where mask is True are ignored (set to -inf before softmax).

    Returns:
        output: Attention output of shape (batch_size, seq_len_q, d_v)
        attn_weights: Attention weights of shape (batch_size, seq_len_q, seq_len_k)
    """
    d_k = Q.size(-1)

    # Compute raw attention scores: (batch_size, seq_len_q, seq_len_k)
    scores = torch.matmul(Q, K.transpose(-2, -1))

    # TODO: Scale the scores by the square root of d_k

    # TODO: Apply the mask (if provided) by setting masked positions to -inf

    # TODO: Apply softmax over the last dimension to get attention weights

    # TODO: Compute the final output as the weighted sum of V

    return output, attn_weights


if __name__ == "__main__":
    batch_size = 2
    seq_len = 5
    d_k = 8
    d_v = 16

    Q = torch.randn(batch_size, seq_len, d_k)
    K = torch.randn(batch_size, seq_len, d_k)
    V = torch.randn(batch_size, seq_len, d_v)

    output, attn_weights = scaled_dot_product_attention(Q, K, V)

    print("Output shape:       ", output.shape)       # (2, 5, 16)
    print("Attn weights shape: ", attn_weights.shape) # (2, 5, 5)
