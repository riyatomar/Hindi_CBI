1. Keep the Hindi Sentences with their IDs separated with tab in sentences.txt file within data folder.
    - Geo_nios_13ch_0031	ऋतु वर्ष की वह विशिष्ट अवधि है, जिसमें मौसम की दशायें लगभग समान रहती हैं।

2. Run the following command:
    - python3 main.py
 
# Final and Intermediate output files

1. 'processed_sentences.txt' file witin data folder has the preprocessed input sentences. 
    - Geo_nios_13ch_0031	ऋतु वर्ष की वह विशिष्ट अवधि है , जिसमें मौसम की दशायें लगभग समान रहती हैं ।
    
2. 'tagged_output.txt' file witin data folder has tagged output.
    <sent_id=Geo_nios_13ch_0031>
    ऋतु	NNC
    वर्ष	NN
    की	PSP
    वह	PRP
    विशिष्ट	JJ
    अवधि	NN
    है	VM
    ,	SYM
    जिसमें	PRP
    मौसम	NN
    की	PSP
    दशायें	NN
    लगभग	NN
    समान	JJ
    रहती	VM
    हैं	VAUX
    ।	SYM
    </sent_id>

3. 'clause_bounded_output.txt' file within data folder has clause bounded data.
    <sent_id=Geo_nios_13ch_0031>
    ऋतु	NNC	S
    वर्ष	NN	I
    की	PSP	I
    वह	PRP	I
    विशिष्ट	JJ	I
    अवधि	NN	I
    है	VM	E
    ,	SYM	O
    जिसमें	PRP	S
    मौसम	NN	I
    की	PSP	I
    दशायें	NN	I
    लगभग	NN	I
    समान	JJ	I
    रहती	VM	I
    हैं	VAUX	E
    ।	SYM	O
    </sent_id>

4. 'final_output.txt' file within data has the final and post processed output for a given input Hindi sentence.