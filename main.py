from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
import numpy as np
from fractions import Fraction
from math import factorial, sqrt, pi, e, sin, cos, tan, log, radians

Window.clearcolor = (0.04, 0.04, 0.08, 1)

class MathApp(App):
    def build(self):
        self.title = "Math Pro"
        self.steps = ''
        
        root = ScrollView(size_hint=(1,1), bar_width=0)
        main = BoxLayout(orientation='vertical', padding=dp(8), spacing=dp(6), size_hint_y=None)
        main.bind(minimum_height=main.setter('height'))
        
        title = Label(text='MATH PRO', font_size=dp(20), bold=True,
                     color=(0.2,0.8,1,1), size_hint_y=None, height=dp(35))
        main.add_widget(title)
        
        sections = [
            ('🔢', 'Арифметика'),
            ('📐', 'Геометрия'),
            ('📊', 'Статистика'),
            ('∫', 'Анализ'),
            ('📏', 'Алгебра'),
            ('🎲', 'Комбинаторика')
        ]
        
        self.section_grid = GridLayout(cols=3, spacing=dp(4), size_hint_y=None, height=dp(90))
        self.section_btns = {}
        for icon, name in sections:
            btn = Button(text=f'{icon}\n{name}', font_size=dp(10), bold=True,
                        background_color=(0.1,0.1,0.2,1), color=(0.8,0.8,1,1),
                        halign='center', valign='middle')
            btn.bind(on_press=lambda x, n=name: self.select_section(n))
            self.section_btns[name] = btn
            self.section_grid.add_widget(btn)
        main.add_widget(self.section_grid)
        
        self.op_grid = GridLayout(cols=2, spacing=dp(3), size_hint_y=None, height=dp(200))
        main.add_widget(self.op_grid)
        
        self.inp = TextInput(text='', hint_text='Введи значение...', multiline=False,
                            font_size=dp(20), size_hint_y=None, height=dp(50),
                            background_color=(0.06,0.06,0.15,1), foreground_color=(1,1,1,1),
                            padding=[dp(10), dp(10)])
        main.add_widget(self.inp)
        
        self.inp2 = TextInput(text='', hint_text='', multiline=False,
                             font_size=dp(18), size_hint_y=None, height=0, opacity=0,
                             background_color=(0.06,0.06,0.15,1), foreground_color=(1,1,1,1))
        main.add_widget(self.inp2)
        
        self.solve_btn = Button(text='РЕШИТЬ', font_size=dp(22), bold=True,
                               background_color=(0.1,0.8,0.1,1), size_hint_y=None, height=dp(60))
        self.solve_btn.bind(on_press=self.solve)
        main.add_widget(self.solve_btn)
        
        self.res = Label(text='', font_size=dp(24), bold=True,
                        color=(0.2,1,0.2,1), size_hint_y=None, height=dp(50), halign='center')
        main.add_widget(self.res)
        
        self.step_btn = Button(text='📋 Показать решение', font_size=dp(14),
                              background_color=(0.1,0.3,0.7,1), size_hint_y=None, height=dp(35))
        self.step_btn.bind(on_press=lambda x: self.show_steps())
        main.add_widget(self.step_btn)
        
        self.sol = Label(text='', font_size=dp(12), color=(0.7,0.7,1,1),
                        size_hint_y=None, halign='left', valign='top',
                        text_size=(Window.width-dp(20), None))
        self.sol.bind(texture_size=lambda _,v: setattr(self.sol,'height',v[1]))
        main.add_widget(self.sol)
        
        root.add_widget(main)
        return root

    def select_section(self, name):
        for n, btn in self.section_btns.items():
            btn.background_color = (0.05,0.3,0.6,1) if n == name else (0.1,0.1,0.2,1)
        
        ops = {
            'Арифметика': [
                ('Калькулятор', '7+3*2'),
                ('Дроби', '3/4 + 1/2'),
                ('Проценты', '15% от 200'),
                ('Степень', '2^10'),
                ('Корень', '√144'),
                ('НОД и НОК', '24 и 36'),
                ('Округление', '3.14159'),
            ],
            'Геометрия': [
                ('□ Площадь квадрата', 'сторона'),
                ('▭ Площадь прямоуг.', 'стороны'),
                ('△ Площадь треуг.', 'основание, высота'),
                ('○ Площадь круга', 'радиус'),
                ('□ Периметр кв.', 'сторона'),
                ('▭ Периметр прям.', 'стороны'),
                ('○ Длина окр.', 'радиус'),
                ('📦 Объём куба', 'ребро'),
                ('⚽ Объём шара', 'радиус'),
                ('📐 Пифагор', 'катеты'),
                ('sin/cos/tg', 'sin 30'),
            ],
            'Статистика': [
                ('Всё сразу', '5;8;12;7;9'),
                ('Среднее', '5;8;12;7;9'),
                ('Медиана', '5;8;12;7;9'),
                ('Мода', '5;8;12;7;9'),
                ('Размах', '5;8;12;7;9'),
                ('Дисперсия', '5;8;12;7;9'),
            ],
            'Анализ': [
                ('Производная', 'x^2+3x'),
                ('Интеграл', 'x^2 от 0 до 3'),
                ('Предел', 'sin(x)/x x->0'),
            ],
            'Алгебра': [
                ('Уравнение', 'x^2-5x+6=0'),
                ('Система', 'x+y=5;x-y=1'),
                ('Упростить', 'x^2+2x+1'),
                ('Разложить', 'x^2-4'),
                ('Раскрыть', '(x+1)^2'),
            ],
            'Комбинаторика': [
                ('Факториал', '5!'),
                ('C(n,k)', 'C(10,3)'),
                ('A(n,k)', 'A(5,2)'),
                ('P(n)', 'P(4)'),
            ]
        }
        
        self.current_ops = ops.get(name, [])
        self.op_grid.clear_widgets()
        self.op_grid.height = dp(40 * ((len(self.current_ops)+1)//2))
        
        for op_name, hint in self.current_ops:
            btn = Button(text=op_name, font_size=dp(12), bold=True,
                        background_color=(0.08,0.08,0.2,1), color=(0.9,0.9,1,1),
                        halign='center', valign='middle')
            btn.bind(on_press=lambda x, o=op_name, h=hint: self.select_op(o, h))
            self.op_grid.add_widget(btn)
        
        self.inp2.height = 0
        self.inp2.opacity = 0

    def select_op(self, op, hint):
        self.current_op = op
        self.inp.text = ''
        self.inp.hint_text = hint
        
        if op in ['▭ Площадь прямоуг.', '▭ Периметр прям.', '△ Площадь треуг.', 
                  '📐 Пифагор', 'НОД и НОК', 'Система', 'C(n,k)', 'A(n,k)']:
            self.inp2.height = dp(45)
            self.inp2.opacity = 1
            self.inp2.hint_text = 'Второе значение'
        else:
            self.inp2.height = 0
            self.inp2.opacity = 0

    def solve(self, instance):
        e = self.inp.text.strip()
        e2 = self.inp2.text.strip() if self.inp2.opacity else ''
        
        self.steps = f'{self.current_op}\n\n'
        
        try:
            result = self.calculate(e, e2)
            self.res.text = str(result)[:50]
            self.sol.text = self.steps
        except Exception as ex:
            self.res.text = 'Ошибка'
            self.steps += f'❌ {ex}'
            self.sol.text = self.steps

    def calculate(self, e, e2):
        op = self.current_op
        
        if op == 'Калькулятор':
            safe = {'sin':sin,'cos':cos,'tan':tan,'sqrt':sqrt,'pi':pi,'e':e,'log':log}
            r = eval(e.replace('^','**'), {"__builtins__":{}}, safe)
            self.steps += f'{e} = {r}'
            return round(r, 6) if isinstance(r, float) else r
        
        if op == 'Дроби':
            r = eval(e, {"__builtins__":{}}, {"Fraction":Fraction})
            self.steps += f'{e}\n= {r}\n≈ {float(r):.4f}'
            return f'{r}'
        
        if op == 'Проценты':
            p, n = e.split('от')
            p = float(p.replace('%','').strip())
            n = float(n.strip())
            r = n * p / 100
            self.steps += f'{p}% от {n} = {r}'
            return r
        
        if op == 'Степень':
            b, exp = e.replace('^',' ').split()
            r = float(b) ** float(exp)
            self.steps += f'{b}^{exp} = {r}'
            return r
        
        if op == 'Корень':
            r = sqrt(float(e))
            self.steps += f'√{e} = {r:.6f}'
            return round(r, 6)
        
        if op == 'НОД и НОК':
            a, b = int(e), int(e2)
            g = np.gcd(a, b)
            l = a*b//g
            self.steps += f'НОД({a},{b}) = {g}\nНОК({a},{b}) = {l}'
            return f'НОД={g}, НОК={l}'
        
        if op == 'Округление':
            n = float(e)
            r = round(n, 2)
            self.steps += f'{n} → {r}'
            return r
        
        if op == '□ Площадь квадрата':
            a = float(e); s = a**2
            self.steps += f'S = a² = {a}² = {s}'
            return s
        
        if op == '▭ Площадь прямоуг.':
            a, b = float(e), float(e2); s = a*b
            self.steps += f'S = {a}×{b} = {s}'
            return s
        
        if op == '△ Площадь треуг.':
            a, h = float(e), float(e2); s = 0.5*a*h
            self.steps += f'S = ½×{a}×{h} = {s}'
            return s
        
        if op == '○ Площадь круга':
            r = float(e); s = pi*r**2
            self.steps += f'S = π×{r}² = {s:.4f}'
            return round(s, 4)
        
        if op == '□ Периметр кв.':
            a = float(e); p = 4*a
            self.steps += f'P = 4×{a} = {p}'
            return p
        
        if op == '▭ Периметр прям.':
            a, b = float(e), float(e2); p = 2*(a+b)
            self.steps += f'P = 2({a}+{b}) = {p}'
            return p
        
        if op == '○ Длина окр.':
            r = float(e); c = 2*pi*r
            self.steps += f'C = 2π×{r} = {c:.4f}'
            return round(c, 4)
        
        if op == '📦 Объём куба':
            a = float(e); v = a**3
            self.steps += f'V = {a}³ = {v}'
            return v
        
        if op == '⚽ Объём шара':
            r = float(e); v = 4/3*pi*r**3
            self.steps += f'V = 4/3π×{r}³ = {v:.4f}'
            return round(v, 4)
        
        if op == '📐 Пифагор':
            a, b = float(e), float(e2); c = sqrt(a**2+b**2)
            self.steps += f'c = √({a}²+{b}²) = {c:.4f}'
            return round(c, 4)
        
        if op == 'sin/cos/tg':
            f, ang = e.split()
            ang = float(ang)
            funcs = {'sin':sin,'cos':cos,'tg':tan}
            r = funcs[f](radians(ang))
            self.steps += f'{f}({ang}°) = {r:.4f}'
            return round(r, 4)
        
        if op in ['Всё сразу','Среднее','Медиана','Мода','Размах','Дисперсия']:
            nums = [float(x.strip()) for x in e.replace(',',';').split(';')]
            avg = sum(nums)/len(nums)
            sorted_nums = sorted(nums)
            n = len(nums)
            
            self.steps += f'Числа: {nums}\nКол-во: {n}\n\n'
            self.steps += f'Среднее: {avg:.4f}\n'
            
            if n%2==0:
                med = (sorted_nums[n//2-1]+sorted_nums[n//2])/2
            else:
                med = sorted_nums[n//2]
            self.steps += f'Медиана: {med:.4f}\n'
            
            from collections import Counter
            mode_data = Counter(nums).most_common(1)[0]
            self.steps += f'Мода: {mode_data[0]} ({mode_data[1]} раз)\n'
            
            rng = max(nums)-min(nums)
            self.steps += f'Размах: {rng}\nМин: {min(nums)}, Макс: {max(nums)}\n'
            
            var = sum((x-avg)**2 for x in nums)/n
            std = sqrt(var)
            self.steps += f'Дисперсия: {var:.4f}\nСтд откл: {std:.4f}'
            
            return f'μ={avg:.2f}, σ={std:.2f}'
        
        if op == 'Производная':
            import sympy as sp
            x = sp.Symbol('x')
            f = sp.sympify(e.replace('^','**'))
            d = sp.diff(f, x)
            self.steps += f'f(x) = {f}\nf\'(x) = {d}'
            return str(d)
        
        if op == 'Интеграл':
            import sympy as sp
            x = sp.Symbol('x')
            if 'от' in e:
                parts = e.split('от')
                f_str = parts[0].strip()
                lims = parts[1].split('до')
                a, b = float(lims[0]), float(lims[1])
                f = sp.sympify(f_str.replace('^','**'))
                r = float(sp.N(sp.integrate(f, (x, a, b))))
                F = sp.integrate(f, x)
                self.steps += f'∫{f}dx от {a} до {b}\n= [{F}]\n= {r:.6f}'
                return round(r, 6)
            else:
                f = sp.sympify(e.replace('^','**'))
                r = sp.integrate(f, x)
                self.steps += f'∫{f}dx = {r} + C'
                return f'{r} + C'
        
        if op == 'Предел':
            import sympy as sp
            x = sp.Symbol('x')
            parts = e.split('x->')
            f = sp.sympify(parts[0].strip().replace('^','**'))
            pt = float(parts[1].strip())
            r = sp.limit(f, x, pt)
            self.steps += f'lim({f}) x→{pt} = {r}'
            return str(r)
        
        if op == 'Уравнение':
            import sympy as sp
            x = sp.Symbol('x')
            l, r = e.split('=') if '=' in e else (e, '0')
            eq = sp.Eq(sp.sympify(l.replace('^','**')), sp.sympify(r.replace('^','**')))
            sol = sp.solve(eq, x)
            self.steps += f'{eq}\nx = {sol}'
            return str(sol)
        
        if op == 'Система':
            import sympy as sp
            x, y = sp.symbols('x y')
            eqs = []
            for eq in e.split(';'):
                l, r = eq.strip().split('=')
                eqs.append(sp.Eq(sp.sympify(l.replace('^','**')), sp.sympify(r.replace('^','**'))))
            sol = sp.solve(eqs, (x, y))
            self.steps += f'{eqs}\n{sol}'
            return str(sol)
        
        if op == 'Упростить':
            import sympy as sp
            r = sp.simplify(sp.sympify(e.replace('^','**')))
            self.steps += f'{e} → {r}'
            return str(r)
        
        if op == 'Разложить':
            import sympy as sp
            r = sp.factor(sp.sympify(e.replace('^','**')))
            self.steps += f'{e} → {r}'
            return str(r)
        
        if op == 'Раскрыть':
            import sympy as sp
            r = sp.expand(sp.sympify(e.replace('^','**')))
            self.steps += f'{e} → {r}'
            return str(r)
        
        if op == 'Факториал':
            n = int(e.replace('!',''))
            r = factorial(n)
            self.steps += f'{n}! = {r}'
            return r
        
        if op == 'C(n,k)':
            n, k = int(e), int(e2)
            r = factorial(n)//(factorial(k)*factorial(n-k))
            self.steps += f'C({n},{k}) = {r}'
            return r
        
        if op == 'A(n,k)':
            n, k = int(e), int(e2)
            r = factorial(n)//factorial(n-k)
            self.steps += f'A({n},{k}) = {r}'
            return r
        
        if op == 'P(n)':
            n = int(e)
            r = factorial(n)
            self.steps += f'P({n}) = {r}'
            return r

    def show_steps(self):
        self.sol.text = self.steps if self.steps else 'Сначала нажми РЕШИТЬ'

MathApp().run()
