<!-- Extracted using strategy: text -->

|the input sequence c|entered aro|und the respec|tive output position|. This would|increase th|e maximum|
|---|---|---|---|---|---|---|
|path length to_ O_(_n/_|_r_). We plan|to investigate|this approach furt|her in future|work.||
|<br>|<br>|<br>|<br>|<br>|<br>||
|A single convolutio|nal layer wi|th kernel widt|h_ k < n_ does not c|onnect all p|airs of inpu|t and output|
|positions. Doing so|requires a st|ack of_ O_(_n/k_|) convolutional lay|ers in the cas|e of contig|uous kernels,|
|or_ O_(_logk_(_n_)) in th|e case of d|ilated convolu|tions [15], increas|ing the leng|th of the l|ongest paths|
|between any two po|sitions in t|he network. C|onvolutional layers|are general|ly more ex|pensive than|
|recurrent layers, by<br>|a factor of<br>|_k_. Separable<br>|convolutions [6], <br>|however, d<br>|ecrease the<br>|complexity<br>|
|considerably, to_ O_(|_k · n · d_ +|_ n · d_2). Even|with_ k_ = _n_, howe|ver, the co|mplexity of|a separable|
|convolution is equa|l to the com|bination of a s|elf-attention layer a|nd a point-|wise feed-f|orward layer,|
|the approach we tak|e in our mo|del.|||||
|<br>|<br>|<br>|||||
|As side beneﬁt, self-|attention co|uld yield more|interpretable mode|ls. We inspe|ct attention|distributions|
|from our models an|d present an|d discuss exa|mples in the append|ix. Not only|do individ|ual attention|
|heads clearly learn t|o perform d|ifferent tasks,|many appear to exh|ibit behavio|r related to|the syntactic|
|and semantic struct|ure of the se|ntences.|||||
|<br><br>|||||||
|**5**<br>**Training**|||||||
||||||||
|This section describ|es the traini|ng regime for|our models.||||
|<br><br>|<br>|<br>|||||
|**5.1**<br>**Training Dat**|** a and Batc**|**   hing**|||||
|<br>|<br>|<br>|||||
|We trained on the|standard W|MT 2014 Eng|lish-German data|set consistin|g of about|4.5 million|
|sentence pairs. Sen|tences wer|e encoded usi|ng byte-pair encod|ing [3], whi|ch has a sh|ared source-|
|target vocabulary of|about 3700|0 tokens. For|English-French, we|used the si|gniﬁcantly|larger WMT|
|2014 English-Frenc|h dataset co|nsisting of 36|M sentences and s|plit tokens i|nto a 32000|word-piece|
|vocabulary [31]. Se|ntence pairs|were batched t|ogether by approxi|mate sequen|ce length. E|ach training|
|batch contained a s|et of senten|ce pairs conta|ining approximate|ly 25000 so|urce token|s and 25000|
|target tokens.|||||||
|<br><br>|||||||
|**5.2**<br>**Hardware an**|** d Schedule**||||||
|<br>|<br>|<br>|||||
|We trained our mo|dels on one|machine with|8 NVIDIA P100|GPUs. For|our base m|odels using|
|the hyperparameter|s described|throughout th|e paper, each traini|ng step took|about 0.4|seconds. We|
|trained the base mo|dels for a tot|al of 100,000|steps or 12 hours. F|or our big m|odels,(desc|ribed on the|
|bottom line of table|3), step tim|e was 1.0 sec|onds. The big mo|dels were tr|ained for 3|00,000 steps|
|(3.5 days).|||||||
|<br><br>|||||||
|**5.3**<br>**Optimizer**|||||||
||||||||
|||||_−_9|||
|We used the Adam|optimizer [|7] with_ β_1 =|0_._9,_ β_2 = 0_._98 an|_ ϵ_ = 10.|We varied|the learning|
|rate over the course|of training,|<br>      according to|<br>        the formula:||||
|<br>|<br><br>|<br>|<br>||||
|_lrate_|=_ d−_0_._5<br>model _·_ m|in(_step_num_|_−_0_._5_, step_num ·_|_ warmup_s_|_teps−_1_._5)|(3)|
||||||||
|This corresponds to|increasing|the learning r|ate linearly for the|ﬁrst_ warm_|_ up_steps_ tr|aining steps,|
|and decreasing it th|ereafter pro|portionally to|the inverse square|root of the|step numb|er. We used|
|_warmupsteps_ =|4000.||||||
|_<br><br>|||||||
|**5.4**<br>**Regularizatio**|**n**||||||
||||||||
|We employ three ty|pes of regul|arization durin|g training:||||
|<br>|||||||
|**Residual Dropout**|We apply|dropout [27] t|o the output of eac|h sub-layer,|before it is|added to the|
|sub-layer input and|normalized.|In addition, w|e apply dropout to|the sums of|the embedd|ings and the|
|positional encoding|s in both th|e encoder and|decoder stacks. F|or the base|model, we|use a rate of|
|_Pdrop_ = 0_._1.|||||||

