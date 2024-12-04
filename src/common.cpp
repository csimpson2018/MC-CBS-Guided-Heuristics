#include "common.h"

std::ostream& operator<<(std::ostream& os, const Path& path)
{
	for (const auto& state : path)
	{
		os << state.location; // << "(" << state.is_single() << "),";
	}
	return os;
}


bool isSamePath(const Path& p1, const Path& p2)
{
	if (p1.size() != p2.size())
		return false;
	for (unsigned i = 0; i < p1.size(); i++)
	{
		if (p1[i].location != p2[i].location)
			return false;
	}
	return true;
}

vector<double> softmax(const vector<double>& logits) {
    double max_logit = *std::max_element(logits.begin(), logits.end());

    std::vector<double> exps(logits.size());
    for (size_t i = 0; i < logits.size(); ++i) {
        exps[i] = std::exp(logits[i] - max_logit);
    }

    double sum_exps = 0.0;
    for (double exp_val : exps) {
        sum_exps += exp_val;
    }

    std::vector<double> probabilities(logits.size());
    for (size_t i = 0; i < logits.size(); ++i) {
        probabilities[i] = exps[i] / sum_exps;
    }

    return probabilities;
}


vector<double> epsilon_greedy(const vector<double>& h_weights) {

    std::vector<double> probabilities(h_weights.size());
    
	if (h_weights.at(0) > h_weights.at(1))
	{
		probabilities.at(0) = .95;
		probabilities.at(1) = .05;
	}
	else
	{
		probabilities.at(0) = .05;
		probabilities.at(1) = .95;
	}

    return probabilities;
}
