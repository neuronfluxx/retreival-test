<!-- Extracted using strategy: text -->

|Table 1: Maxi|mum path length|s, per-layer c|omp|lexity and minimum|number of seque|ntial operations|
|---|---|---|---|---|---|---|
|for different la|yer types. _n_ is t|he sequence|lengt|h,_ d_ is the represen|tation dimension|,_ k_ is the kernel|
|size of convolu|tions and_ r_ the|size of the n|eighb|orhood in restricted|self-attention.||
|<br>|<br>|<br>|<br>|<br> <br>|<br><br>||
|Layer Typ|e|Complexi|ty pe|r Layer<br>Sequenti|al<br>Maximum P|ath Length|
|||<br>|<br>|<br><br>Operatio<br>|<br>ns||
|Self-Atten|tion|_O_(_n_<br>|2 _· d_<br>|)<br>_O_(1)<br>|_O_(|1)|
|Recurrent||_O_(_n_<br>|_ · d_2<br>|)<br>_O_(_n_)<br>|_O_(|_n_)|
|Convolutio|nal|_O_(_k ·_|_ n · d_|2)<br>_O_(1)|_O_(_log_|_k_(_n_))|
|Self-Atten|tion (restricted)|_O_(_r _|_ · n · _|_ d_)<br>_O_(1)|_O_(_n_|_/r_)|
|<br>|<br>||||||
|bottoms of the|encoder and dec|oder stacks.|The|positional encodings|have the same d|imension_ d_model|
|as the embeddi|ngs, so that the|two can be s|umm|ed. There are many|choices of positi|onal encodings,|
|learned and ﬁx|ed [8].||||||
|<br>|<br>||||||
|In this work, w|e use sine and c|osine functi|ons o|f different frequenc|ies:||
|||<br>|<br>|<br>|<br>||
|||_PE_(_pos,_2_i_)|=_ si_|_ n_(_pos/_100002_i/d_mo|del)||
|||<br>|<br>|<br>|||
||_P_|_E_(_pos,_2_i_+1)|=_ co_|_ s_(_pos/_100002_i/d_mo|del)||
|||<br>|<br>|<br>|||
|where_ pos_ is th|e position and_ i_|is the dimen|sion.|That is, each dime|nsion of the posi|tional encoding|
|corresponds to|a sinusoid. The|wavelengths|form|a geometric progre|ssion from 2_π_ to|10000_ ·_ 2_π_. We|
|chose this fun|ction because w|e hypothesiz|ed it|would allow the m|odel to easily le|arn to attend by|
|relative positio|ns, since for an|y ﬁxed offse|t_ k_,|_ PEpos_+_k_ can be rep|resented as a lin|ear function of|
|_PEpos_.|||||||
||||||||
|We also experi|mented with usi|ng learned p|ositio|nal embeddings [8|] instead, and fou|nd that the two|
|versions produ|ced nearly iden|tical results|(see|Table 3 row (E)).|We chose the sin|usoidal version|
|because it may|allow the mode|l to extrapol|ate to|sequence lengths l|onger than the on|es encountered|
|during training|.||||||
|<br><br>|<br>||||||
|**4**<br>**Why Se**|** lf-Attention**||||||
|<br>|<br>||||||
|In this section|we compare v|arious aspec|ts of|self-attention layer|s to the recurre|nt and convolu-|
|tional layers c<br>|ommonly used f<br>|or mapping<br>|one v<br>|ariable-length sequ<br>|ence of symbol<br>|representations<br>|
|(_x_1_, ..., xn_) to|another sequen|ce of equal|lengt|h (_z_1_, ..., zn_), with|_xi, zi ∈_R_d_, su|ch as a hidden|
|layer in a typic|al sequence tran|sduction enc|oder|or decoder. Motiva|<br>ting our use of s|elf-attention we|
|consider three|desiderata.||||||
|<br>|<br>||||||
|One is the tota|l computational|complexity|per la|yer. Another is the|amount of comp|utation that can|
|be parallelized|, as measured b|y the minimu|m nu|mber of sequential|operations requi|red.|
|<br>|<br>|<br>|<br>|<br>|<br>|<br>|
|The third is th|e path length bet|ween long-r|ange|dependencies in th|e network. Learn|ing long-range|
|dependencies i|s a key challeng|e in many s|equen|ce transduction tas|ks. One key fact|or affecting the|
|ability to learn|such dependen|cies is the le|ngth|of the paths forwar|d and backward|signals have to|
|traverse in the|network. The s|horter these|paths|between any comb|ination of positi|ons in the input|
|and output seq|uences, the easie|r it is to lear|n lon|g-range dependenci|es [11]. Hence w|e also compare|
|the maximum|path length betw|een any two|inpu|t and output positio|ns in networks c|omposed of the|
|different layer|types.||||||
|<br>|<br>||||||
|As noted in Tab|le 1, a self-atten|tion layer co|nnect|s all positions with a|constant numbe|r of sequentially|
|executed oper|ations, whereas|a recurrent|layer|requires _O_(_n_) seq|uential operatio|ns. In terms of|
|computational|complexity, sel|f-attention l|ayers|are faster than recu|rrent layers whe|n the sequence|
|length _n_ is sm|aller than the r|epresentatio|n di|mensionality _d_, wh|ich is most ofte|n the case with|
|sentence repre|sentations used b|y state-of-th|e-art|models in machine|translations, suc|h as word-piece|
|[31] and byte-|pair [25] represe|ntations. To|impr|ove computational|performance for|tasks involving|
|very long sequ|ences, self-attent|ion could be|restr|icted to considering|only a neighborh|ood of size_ r_ in|

