# OCO-2 CO2 peak detector
> OCO-2 Satellite CO2 peak detector. 


This file will become your README and also the index of your documentation.

## Install

`pip install oco2peak`

## How to use

Fill me in please! Don't forget code examples:

## Data

```python
config = '../configs/config.json'
datasets = Datasets(config)
datasets.get_files_urls('result_for_oco2_1808')
```




    ['https://storage.gra.cloud.ovh.net/v1/AUTH_2aaacef8e88a4ca897bb93b984bd04dd/oco2//datasets/oco-2/peaks-detected/result_for_oco2_1808.csv']



### Upload a file

```python
datasets.upload(mask='../*.md', prefix="/Trash/",content_type='text/text')
```

    100%|██████████| 2/2 [00:00<00:00,  6.04it/s]


### Delete files

```python
datasets.delete_files("/Trash/", dry_run=False)
```

    deleting /Trash/CONTRIBUTING.md
    deleting /Trash/README.md

