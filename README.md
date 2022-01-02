# miRNAtpa
Micro RNA target prodiction analysis.

## Requirements

* Git
* Python 3.6 or later

## Install

```bash
git clone https://github.com/ualich/miRNAtpa.git
cd miRNAtpa
pip install .
```

## Usage

To run new analysis, create a directory inside `analyses`. Add input data in the subdirectory `input`. Results will be generated in subdirecotry `results`.

See directory `anayses/example` for exact filesystem structure.

Run the command

```bash
python3 mirnatpa/run.py <analysis_name> <regions>
```

Where

* `analyses_name` - alphanumerical name of the analysis
* `regions` - space separated names of regions used for expression analysis, possible values: 

Regions available: adipocyte_1, arachnoid_mater_1, artery_1, colon_1, small_intestine_1, dura_mater_1, brain_1, bladder_1, skin_1, myocardium_1, bone_1, liver_1, lung_1, stomach_1, spleen_1, muscle_1, gallbladder_1, fascia_1, epididymis_1, nerve_nervus_intercostalis_1, kidney_1, thyroid_1, testis_1, tunica_albuginea_1, myocardium_2, lung_2, liver_2, kidney_2, colon_2, muscle_2, small_intestine_duodenum_2, pancreas_2, small_intestine_jejunum_2, kidney_glandula_suprarenalis_2, brain_thalamus_2, bone_marrow_2, spinal_cord_2, pleura_2, brain_pituitary_gland_2, kidney_cortex_renalis_2, stomach_2, nerve_not_specified_2, esophagus_2, prostate_2, adipocyte_2, skin_2, spleen_2, brain_white_matter_2, brain_nucleus_caudatus_2, kidney_medulla_renalis_2, thyroid_2, brain_gray_matter_2, lymph_node_2, brain_cerebral_cortex_temporal_2, brain_cerebral_cortex_frontal_2, dura_mater_2, artery_2, brain_cerebral_cortex_occipital_2, vein_2, brain_cerebellum_2, testis_2
