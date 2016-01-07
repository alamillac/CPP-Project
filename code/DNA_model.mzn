include "alldifferent.mzn";


%Constants
int: num_nucleotides_in_original_DNA;
int: num_nucleotides;
int: num_DNA_pieces;
int: max_nucleotides_in_DNA;

set of int: DNA_pieces = 1..num_DNA_pieces;
set of int: Nucleotides = 0..num_nucleotides;  %0 means void

array[DNA_pieces] of 1..max_nucleotides_in_DNA: sizes_DNA_pieces;
array[DNA_pieces, 1..max_nucleotides_in_DNA] of Nucleotides: DNA_nucleotides;

%Program settings
int: min_k_value;

%Variables
array[DNA_pieces] of var DNA_pieces: original_DNA_order;
array[1..num_DNA_pieces-1] of var int: k;

%Rules
constraint alldifferent(original_DNA_order);
constraint sum(sizes_DNA_pieces) - sum(k) = num_nucleotides_in_original_DNA;
constraint forall(i in 1..num_DNA_pieces-1) (k[i] > min_k_value);

constraint forall(i in 1..num_DNA_pieces-1) (
                if sizes_DNA_pieces[original_DNA_order[i]] - k[i] > 0 then
                    forall(j in 1..max_nucleotides_in_DNA) (
                        if j <= k[i] then
                            DNA_nucleotides[original_DNA_order[i], sizes_DNA_pieces[original_DNA_order[i]] - k[i] + j] = DNA_nucleotides[original_DNA_order[i+1], j]
                        else true endif
                    )
                else false endif
            );

solve satisfy;
