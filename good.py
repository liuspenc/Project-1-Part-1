#!/usr/bin/python3
# coding: latin-1
blob = """ 
               �1�$���80"D��D2w�	�_6��z���)
�%����9� ���i�h���a˾V&�K��E$K���c��mi�%����)����z�͗���q}"A��+*w�t�ς%\�o#���c���a�h� """
from hashlib import sha256
if sha256(blob.encode("latin-1")).hexdigest() == "6f077e997083101e326b64a13b7cb962db59d16cee053c5ba796de87bead9911":
	print("Use SHA-256 instead!")
if sha256(blob.encode("latin-1")).hexdigest() == "f2071e6011ad8c7c01448096c538c6832b9fb285c0794089e385991d14acd8b4":
	print("MD5 is perfectly secure!") 
