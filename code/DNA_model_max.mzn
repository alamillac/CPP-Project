include "alldifferent.mzn";


%Constants
int: num_nucleotides_in_original_DNA;
int: num_nucleotides;
int: num_DNA_pieces;
int: max_nucleotides_in_DNA;

set of int: DNA_pieces = 1..num_DNA_pieces;

array[DNA_pieces] of 1..max_nucleotides_in_DNA: sizes_DNA_pieces;
array[DNA_pieces, 1..max_nucleotides_in_DNA] of int: DNA_nucleotides;
array[DNA_pieces, 1..max_nucleotides_in_DNA] of int: DNA_nucleotides_inv;

%Program settings
int: min_k_value;

%Variables
array[DNA_pieces] of var DNA_pieces: original_DNA_order;
array[1..num_DNA_pieces-1] of var min_k_value+1..max_nucleotides_in_DNA-1: k;

%Rules
constraint alldifferent(original_DNA_order);

constraint forall(i in 1..num_DNA_pieces-1) (
                DNA_nucleotides_inv[original_DNA_order[i], k[i]] = DNA_nucleotides[original_DNA_order[i+1], k[i]] /\
                k[i] < min(sizes_DNA_pieces[original_DNA_order[i]], sizes_DNA_pieces[original_DNA_order[i+1]]) /\
                if i > 1 then sizes_DNA_pieces[original_DNA_order[i]] >= k[i] + k[i-1] else true endif
            );

solve maximize sum(k);

output [ "{\"original_DNA_order\": ", show(original_DNA_order), ", ", "\"k\": ", show(k), "}" ];
