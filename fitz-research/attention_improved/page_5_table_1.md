|Col1|Col2|Col3|Col4|O|Col6|
|---|---|---|---|---|---|
||MultiHe|ad(_Q, K, V_ )|= Concat(head1|_, ...,_ headh)_W O_||
|||||<br>||
|||where headi|= Attention(_QW_|_Q_<br>_i , KW K_<br>_i , V W V_<br>_i_ )||
|||<br>||<br> <br> <br><br>||
|Where the<br>|projections are par<br>|ameter matrice|s_ W Q_<br>_i_<br>_∈_R_d_model_×_|_dk_,_ W K_<br>_i_<br>_∈_R_d_model_×dk_,_ W_|_V_<br>_i_<br>_∈_R_d_model_×dv_|
|and_ W O ∈_|R_hdv×d_model.|||||
|||||||
|In this wo|rk we employ _h_|= 8 parallel|attention layers,|or heads. For each o|f these we use|
|||||||
|_dk_ =_ dv_ =|_ d_model_/h_ = 64.|ue to the redu|ed dimension of|each head, the total co|putational cost|
|<br>is similar t|o that of single-he|ad attention wi|th full dimensio|nality.||
|<br><br>|<br>|<br>|<br>|||
|**3.2.3**<br>**Ap**|**plications of Atte**|**  ntion in our M**|**     odel**|||
|<br>|<br>|<br>|<br>|||
|The Transf|ormer uses multi-|head attention|in three different|ways:||
|<br>|<br>|<br>|<br>|<br>||
|_•_ In|"encoder-decode|r attention" la|yers, the queries|come from the previous|decoder layer,|
|an|d the memory ke|ys and values|come from the o|utput of the encoder. Th|is allows every|
|p|osition in the deco|der to attend o|ver all positions|in the input sequence. T|his mimics the|
|ty|pical encoder-dec|oder attention|mechanisms in|sequence-to-sequence|models such as|
|[3|1, 2, 8].|||||
|<br>|<br>|||||
|_•_ T|he encoder contai|ns self-attentio|n layers. In a se|lf-attention layer all of t|he keys, values|
|an|d queries come fr|om the same p|lace, in this case|, the output of the previ|ous layer in the|
|en|coder. Each posit|ion in the enco|der can attend to|all positions in the previ|ous layer of the|
|en<br>|<br>coder.<br>|<br>|<br>|<br>|<br>|
|_•_ Si|milarly, self-atten|tion layers in th|e decoder allow|each position in the deco|der to attend to|
|al|l positions in the|decoder up to a|nd including tha|t position. We need to p|revent leftward|
|in|formation ﬂow in|the decoder to|preserve the auto|-regressive property. We|implement this|
|in|side of scaled dot-|product attenti|on by masking ou|t (setting to_ −∞_) all val|ues in the input|
|of|the softmax whic|h correspond t|o illegal connect|ions. See Figure 2.||
|<br><br>|<br>|<br>|<br>|||
|**3.3**<br>**Posit**|**ion-wise Feed-Fo**|** rward Netwo**|**  rks**|||
|<br>|<br>|<br>|<br>|||
|In addition|to attention sub-|layers, each of|the layers in ou|r encoder and decoder c|ontains a fully|
|connected|feed-forward netw|ork, which is|applied to each p|osition separately and i|dentically. This|
|consists of|two linear transfo|rmations with|a ReLU activatio|n in between.||
|||<br>|<br>|<br>||
|||||||
|||FFN(_x_) = m|ax(0_, xW_1 +_ b_1|)_W_2 +_ b_2|(2)|
||||<br>|<br>||
|While the l|inear transformati|ons are the sam|e across different|positions, they use diffe|rent parameters|
|from layer|to layer. Anoth|er way of des|cribing this is a|s two convolutions with|kernel size 1.|
|The dimen|sionality of input|and output is|_d_model = 512,|and the inner-layer has|dimensionality|
|_dff_ = 204|8.|||||
|<br><br>||||||
|**3.4**<br>**Emb**|**eddings and Soft**|**  max**||||
|<br>|<br>|<br>||||
|Similarly t|o other sequence|transduction m|odels, we use le|arned embeddings to co|nvert the input|
|tokens and|output tokens to v|ectors of dimen|sion_ d_model. We|also use the usual learned|linear transfor-|
|mation and|softmax function|to convert the|decoder output t|o predicted next-token p|robabilities. In|
|our model,<br>|we share the sam<br>|e weight matrix<br>|between the tw<br>|o embedding layers and t<br>|he pre-softmax<br>  _√_|
|linear trans|formation, similar|to [24]. In the|embedding layer|s, we multiply those weig|hts by _d_model.|
|||||||
|**3.5**<br>**Posit**|**ional Encoding**|||||
|<br>|<br>|||||
|Since our|model contains no|recurrence and|no convolution, i|n order for the model to|make use of the|
|order of th|e sequence, we mu|st inject some|information abou|t the relative or absolute|position of the|
|tokens in t|he sequence. To t|his end, we ad|d "positional enc|odings" to the input em|beddings at the|

