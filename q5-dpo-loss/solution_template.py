import torch


def dpo_loss(chosen_logprobs_policy, rejected_logprobs_policy,
             chosen_logprobs_ref, rejected_logprobs_ref, beta=0.1):
    """
    Compute the Direct Preference Optimization (DPO) loss.

    Args:
        chosen_logprobs_policy:   Log probabilities of chosen responses under the policy model.
                                  Shape: (batch_size,)
        rejected_logprobs_policy: Log probabilities of rejected responses under the policy model.
                                  Shape: (batch_size,)
        chosen_logprobs_ref:      Log probabilities of chosen responses under the reference model.
                                  Shape: (batch_size,)
        rejected_logprobs_ref:    Log probabilities of rejected responses under the reference model.
                                  Shape: (batch_size,)
        beta:                     Temperature parameter controlling deviation from the reference policy.
                                  Scalar float.

    Returns:
        loss: Scalar DPO loss averaged over the batch.
    """

    # TODO: Compute the log ratio of the policy to the reference for chosen responses.
    #       chosen_log_ratio shape: (batch_size,)

    # TODO: Compute the log ratio of the policy to the reference for rejected responses.
    #       rejected_log_ratio shape: (batch_size,)

    # TODO: Compute the DPO loss using the log ratios and beta.
    #       Hint: the loss involves a sigmoid over the scaled difference of the two log ratios.
    #       loss shape: scalar

    # -------------------------------------------------------------------------
    # WRITTEN ANSWER: In plain English, explain below why the DPO loss can
    # become unstable during training and how you would address it.
    #
    # YOUR EXPLANATION HERE:
    #
    # -------------------------------------------------------------------------

    return loss


if __name__ == "__main__":
    torch.manual_seed(42)
    batch_size = 4

    chosen_logprobs_policy   = torch.tensor([-1.2, -0.8, -1.5, -0.9])
    rejected_logprobs_policy = torch.tensor([-2.1, -1.9, -2.4, -2.0])
    chosen_logprobs_ref      = torch.tensor([-1.0, -1.0, -1.0, -1.0])
    rejected_logprobs_ref    = torch.tensor([-1.0, -1.0, -1.0, -1.0])

    loss = dpo_loss(
        chosen_logprobs_policy,
        rejected_logprobs_policy,
        chosen_logprobs_ref,
        rejected_logprobs_ref,
    )

    print("DPO loss:", loss.item())
