import wave
import struct
import math

def gerar_som(nome_arquivo, frequencia=440, duracao=0.5, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duracao)

    wav_file = wave.open(nome_arquivo, 'w')
    wav_file.setparams((1, 2, sample_rate, n_samples, "NONE", "not compressed"))

    for i in range(n_samples):
        t = float(i) / sample_rate
        valor = volume * math.sin(2 * math.pi * frequencia * t)
        data = struct.pack('<h', int(valor * 32767))
        wav_file.writeframesraw(data)

    wav_file.close()


# 💰 Som de cashout (subindo, mais agradável)
gerar_som("cashout.wav", frequencia=800, duracao=0.4)

# 💥 Som de crash (grave e mais longo)
gerar_som("crash.wav", frequencia=200, duracao=0.6)

print("Sons gerados com sucesso!")