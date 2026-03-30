import random
import json
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle


def gerar_multiplicador():
    return 0.1 + (1 / random.random())


class Aviaozinho(App):
    def build(self):
        self.saldo = self.carregar_saldo()
        self.multiplicador = 1.0
        self.crash = 0
        self.voando = False
        self.aposta = 0
        self.historico = []

        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Fundo
        with root.canvas.before:
            Color(0.05, 0.05, 0.08, 1)
            self.rect = Rectangle(size=root.size, pos=root.pos)
        root.bind(size=self._update_rect, pos=self._update_rect)

        # Histórico
        self.label_hist = Label(text="Histórico: ", size_hint=(1, 0.1), markup=True)
        root.add_widget(self.label_hist)

        # Saldo
        self.label_saldo = Label(text=f"Saldo: R$ {self.saldo:.2f}", font_size=22)
        root.add_widget(self.label_saldo)

        # Multiplicador
        self.label_multi = Label(text="1.00x", font_size=40, color=(0,1,0,1))
        root.add_widget(self.label_multi)

        # Status
        self.label_status = Label(text="Faça sua aposta", size_hint=(1, 0.15))
        root.add_widget(self.label_status)

        # 🌐 Multiplayer fake
        self.label_players = Label(text="Jogadores: ", size_hint=(1, 0.15))
        root.add_widget(self.label_players)

        # Input
        self.input_aposta = TextInput(
            hint_text="Valor da aposta",
            multiline=False,
            input_filter='float',
            size_hint=(1, 0.1)
        )
        root.add_widget(self.input_aposta)

        # Botões
        btn_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)

        self.btn_apostar = Button(text="APOSTAR", background_color=(0, 0.6, 1, 1))
        self.btn_apostar.bind(on_press=self.iniciar_rodada)

        self.btn_cashout = Button(text="CASHOUT", background_color=(0, 1, 0, 1))
        self.btn_cashout.bind(on_press=self.cashout_manual)

        btn_layout.add_widget(self.btn_apostar)
        btn_layout.add_widget(self.btn_cashout)
        root.add_widget(btn_layout)

        # Sons
        self.som_cashout = SoundLoader.load('cashout.wav')
        self.som_crash = SoundLoader.load('crash.wav')

        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    # 💾 SALVAR / CARREGAR SALDO
    def carregar_saldo(self):
        try:
            with open("saldo.json", "r") as f:
                return json.load(f)["saldo"]
        except:
            return 1000

    def salvar_saldo(self):
        with open("saldo.json", "w") as f:
            json.dump({"saldo": self.saldo}, f)

    # 📊 Histórico
    def atualizar_historico(self):
        texto = "Histórico: "
        for item in self.historico[-10:]:
            if item == "O":
                texto += "[color=00ff00]●[/color] "
            else:
                texto += "[color=ff0000]●[/color] "
        self.label_hist.text = texto

    # 🌐 Multiplayer fake
    def gerar_jogadores(self):
        nomes = ["Ana", "Carlos", "Pedro", "Lucas", "Marina", "João"]
        texto = "Jogadores:\n"

        for _ in range(random.randint(3, 6)):
            nome = random.choice(nomes)
            valor = random.randint(10, 500)
            texto += f"{nome}: R$ {valor}\n"

        self.label_players.text = texto

    def iniciar_rodada(self, instance):
        if self.voando:
            return

        try:
            aposta = float(self.input_aposta.text)
        except:
            self.label_status.text = "Valor inválido!"
            return

        if aposta <= 0 or aposta > self.saldo:
            self.label_status.text = "Saldo insuficiente!"
            return

        self.aposta = aposta
        self.saldo -= aposta
        self.salvar_saldo()

        self.label_saldo.text = f"Saldo: R$ {self.saldo:.2f}"

        self.multiplicador = 1.0
        self.crash = gerar_multiplicador()
        self.voando = True

        self.gerar_jogadores()

        self.label_status.text = "✈️ Voando..."
        Clock.schedule_interval(self.atualizar_voo, 0.03)

    def atualizar_voo(self, dt):
        if not self.voando:
            return False

        self.multiplicador += 0.02
        self.label_multi.text = f"{self.multiplicador:.2f}x"

        if self.multiplicador >= self.crash:
            self.voando = False
            self.label_status.text = f"💥 Crash em {self.crash:.2f}x"

            self.historico.append("X")
            self.atualizar_historico()

            if self.som_crash:
                self.som_crash.play()

            return False

    def cashout_manual(self, instance):
        if not self.voando:
            return

        ganho = self.aposta * self.multiplicador
        self.saldo += ganho
        self.salvar_saldo()

        self.label_saldo.text = f"Saldo: R$ {self.saldo:.2f}"
        self.label_status.text = f"💰 Cashout: {ganho:.2f}"

        self.historico.append("O")
        self.atualizar_historico()

        if self.som_cashout:
            self.som_cashout.play()

        self.voando = False


if __name__ == "__main__":
    Aviaozinho().run()