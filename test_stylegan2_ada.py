# -*- coding: utf-8 -*-
"""Test.Stylegan2_ada.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RwOIOuGKVdVtwGSNM4h0KXRETdimlnCK
"""

import os
import argparse
import subprocess
import urllib.request

def download_pretrained_model(model_url, model_path):
    if not os.path.exists(model_path):
        print(f"Downloading pretrained model from {model_url} ...")
        urllib.request.urlretrieve(model_url, model_path)
        print("Download complete.")
    else:
        print("Pretrained model already exists at", model_path)

def fine_tune_model(pretrained_model_path, dataset_zip, outdir, gpus, total_kimg, resume=True):
    command = [
        'python', 'train.py',
        f'--outdir={outdir}',
        f'--data={dataset_zip}',
        f'--gpus={gpus}',
        f'--total-kimg={total_kimg}',
        '--snap=10'
    ]
    if resume:
        command.append(f'--resume={pretrained_model_path}')
    print("Starting fine-tuning. Running command:")
    print(" ".join(command))
    subprocess.run(command, check=True)
    print("Fine-tuning completed.")

def generate_images(network_pkl, outdir, seeds, truncation):
    command = [
        'python', 'generate.py',
        f'--outdir={outdir}',
        f'--trunc={truncation}',
        f'--seeds={seeds}',
        f'--network={network_pkl}'
    ]
    print("Generating images. Running command:")
    print(" ".join(command))
    subprocess.run(command, check=True)
    print("Image generation completed.")

def main():
    parser = argparse.ArgumentParser(description="Download a pretrained StyleGAN2-ADA model, fine-tune it on your monkeypox dataset, and generate synthetic images.")
    parser.add_argument('--dataset_zip', type=str, required=True)
    parser.add_argument('--pretrained_url', type=str, default="https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2_ada_pytorch_lsun-bedroom/versions/1/files/stylegan2-ada-pytorch.pkl")
    parser.add_argument('--pretrained_model_path', type=str, default="pretrained_model.pkl")
    parser.add_argument('--outdir', type=str, default="results")
    parser.add_argument('--gpus', type=int, default=1)
    parser.add_argument('--total_kimg', type=int, default=100)
    parser.add_argument('--seeds', type=str, default="0-9")
    parser.add_argument('--trunc', type=float, default=0.7)
    args = parser.parse_args()

    download_pretrained_model(args.pretrained_url, args.pretrained_model_path)

    fine_tune_model(
        pretrained_model_path=args.pretrained_model_path,
        dataset_zip=args.dataset_zip,
        outdir=args.outdir,
        gpus=args.gpus,
        total_kimg=args.total_kimg,
        resume=True
    )

    trained_network_pkl = os.path.join(args.outdir, "network-snapshot-final.pkl")
    if not os.path.exists(trained_network_pkl):
        trained_network_pkl = os.path.join(args.outdir, "network-snapshot-latest.pkl")
    if not os.path.exists(trained_network_pkl):
        raise FileNotFoundError("Could not locate the trained network pickle file in the output directory.")

    generated_outdir = "generated_images"
    generate_images(
        network_pkl=trained_network_pkl,
        outdir=generated_outdir,
        seeds=args.seeds,
        truncation=args.trunc
    )

if __name__ == '__main__':
    main()