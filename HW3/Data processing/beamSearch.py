from math import log
from numpy import array

# Beam Search on data, return q best solutions
def BeamSearch(data, q):
    # Create empty list of sequences
    # The 1.0 is there since we multiply scores, so the first instance is not affected by our initial value
    resultSequences = [[list(), 1.0]]
    # Going over each row to find candidates
    for row in data:
        # Create a list for all candidates in this row (beam)
        allCandidates = list()
        # Expand each candidate
        for i in range(len(resultSequences)):
            # colSeq = Sequence of column numbers in Data
            # score = value of candidate (probability of occurrence)
            colSeq, score = resultSequences[i]

            # Now we iterate over all columns again, to do calculations on our current instance
            for j in range(len(row)):
                # Calculate score when adding extra constraint
                # Since we multiply probabilities, these numbers get very small and we lose view in them.
                # Therefore, we multiply the score with the natural logarithm of the probability.
                # We pick candidates based on the lowest score, therefore we multiply with the negative natural logarithm of the probability
                candidate = [colSeq + [j], score * -log(row[j])]
                # print(candidate)
                allCandidates.append(candidate)
        # Order all candidates by score (lowest score first)
        ordered = sorted(allCandidates, key=lambda tup: tup[1])
        # Select q best
        resultSequences = ordered[:q]
    return resultSequences

# Example: define a sequence of 10 words over a vocab of 5 words (A-E)
        # A    B    C    D    E
data = [[0.1, 0.2, 0.3, 0.4, 0.5],
        [0.5, 0.4, 0.3, 0.2, 0.1],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.5, 0.4, 0.3, 0.2, 0.1],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.5, 0.4, 0.3, 0.2, 0.1],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.5, 0.4, 0.3, 0.2, 0.1],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.5, 0.4, 0.3, 0.2, 0.1]]
data = array(data)
# Give best sequence with q=5
result = BeamSearch(data, 5)
# Print(result)
for seq in result:
    print(seq)