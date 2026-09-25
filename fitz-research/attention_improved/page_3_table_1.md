|Col1|Col2|Figure 1|: The|Transformer -|model arch|itecture.|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|||<br>|<br>|<br>|<br>|<br>|||
|wise fully connec|ted|feed-forwar|d netw|ork. We empl|oy a residua|l conne|ction [10] ar|ound each of|
|the two sub-layer|s, f|ollowed by|layer|normalization|[1]. That i|s, the ou|tput of eac|h sub-layer is|
|LayerNorm(_x_ +|Sub|layer(_x_)),|where|Sublayer(_x_) i|s the functi|on impl|emented by|the sub-layer|
|itself. To facilitate|the|se residual|conne|ctions, all sub-l|ayers in the|model,|as well as th|e embedding|
|layers, produce ou|tpu|ts of dimens|ion_ d_|model = 512.|||||
|<br>|<br>|<br>|<br>|<br>|||||
|**Decoder:**<br>The d|eco|der is also co|mpos|ed of a stack of|_ N_ = 6 iden|tical lay|ers. In addit|ion to the two|
|sub-layers in each|en|coder layer,|the d|ecoder inserts a|third sub-l|ayer, w|hich perform|s multi-head|
|attention over the|outp|ut of the enc|oder s|tack. Similar t|o the encode|r, we em|ploy residua|l connections|
|around each of th|e su|b-layers, fo|llowe|d by layer norm|alization.|We also|modify the|self-attention|
|sub-layer in the d|eco|der stack to|prev|ent positions fr|om attendi|ng to su|bsequent po|sitions. This|
|masking, combine|d w|ith fact that|the o|utput embeddin|gs are offse|t by one|position, en|sures that the|
|predictions for po|sitio|n_ i_ can dep|end on|ly on the know|n outputs a|t positio|ns less than|_ i_.|
|<br><br>|||||||||
|**3.2**<br>**Attention**|||||||||
||||||||||
|An attention funct|ion|can be desc|ribed|as mapping a q|uery and a s|et of ke|y-value pair|s to an output,|
|where the query, k|eys|, values, and|outp|ut are all vector|s. The outp|ut is com|puted as a|weighted sum|
|of the values, whe|re t|he weight as|signed|to each value i|s computed|by a co|mpatibility f|unction of the|
|query with the cor|res|ponding key|.||||||
|<br><br>|<br>|<br>|<br>||||||
|**3.2.1**<br>**Scaled Do**|** t-P**|** roduct Atte**|**  ntion**||||||
|<br>|<br>|<br>|<br>||||||
|We call our partic|ula|r attention "|Scale|d Dot-Product|Attention"|(Figure|2). The inp|ut consists of|
||||||||||
|queries and keys|f d|mension_ dk_|, and|alues of dime|sion_ dv_. W|e comp|te the dot p|oducts of the|

