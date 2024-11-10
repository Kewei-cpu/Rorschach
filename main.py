from typing import List, Optional

import pandas


class Ratio:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.left}:{self.right}"

    def __repr__(self):
        return f"{self.left}:{self.right}"

    def value(self):
        return self.left / self.right

    def abs_value(self):
        return self.left / self.right if self.left > self.right else self.right / self.left

    def abs_diff(self):
        return abs(self.left - self.right)


class TriRatio:
    def __init__(self, left, middle, right):
        self.left = left
        self.middle = middle
        self.right = right

    def __str__(self):
        return f"{self.left}:{self.middle}:{self.right}"

    def __repr__(self):
        return f"{self.left}:{self.middle}:{self.right}"


class Part:
    def __init__(self, part: str):
        # get all the alphabet part
        self.category = ''.join([c for c in part if c.isalpha()])

        # get all the numeric part
        if not any(c.isnumeric() for c in part):
            self.number = 0
        else:
            self.number = int(''.join([c for c in part if c.isnumeric()]))

    def __str__(self):
        return f'{self.category}{self.number if self.number else ''}'

    def __repr__(self):
        return f'{self.category}{self.number if self.number else ''}'


class DQ:
    def __init__(self, dq: str):
        self.dq = dq

    def __str__(self):
        return self.dq

    def __repr__(self):
        return self.dq


class FQ:
    def __init__(self, fq: str):
        self.fq = fq

    def __str__(self):
        return self.fq

    def __repr__(self):
        return self.fq


class Determination:
    def __init__(self, det: str):
        if det[-1] in ('a', 'p'):
            self.det = det[:-1]
            self.motion = det[-1]
        else:
            self.det = det
            self.motion = ''

    def __str__(self):
        return f"{self.det}{self.motion}"

    def __repr__(self):
        return f"{self.det}{self.motion}"

    def active(self):
        return self.motion == 'a'

    def passive(self):
        return self.motion == 'p'


class Content:
    def __init__(self, cont: str):
        self.cont = cont

    def __str__(self):
        return self.cont

    def __repr__(self):
        return self.cont


class Z:
    score_table = {
        1: {"W": 1.0, "A": 4.0, "D": 6.0, "S": 3.5},
        2: {"W": 4.5, "A": 3.0, "D": 5.5, "S": 4.5},
        3: {"W": 5.5, "A": 3.0, "D": 4.0, "S": 4.5},
        4: {"W": 2.0, "A": 4.0, "D": 3.5, "S": 5.0},
        5: {"W": 1.0, "A": 2.5, "D": 5.0, "S": 4.0},
        6: {"W": 2.5, "A": 2.5, "D": 6.0, "S": 6.5},
        7: {"W": 2.5, "A": 1.0, "D": 3.0, "S": 4.0},
        8: {"W": 5.5, "A": 3.0, "D": 3.0, "S": 4.0},
        9: {"W": 5.5, "A": 2.5, "D": 4.5, "S": 5.0},
        10: {"W": 5.5, "A": 4.0, "D": 4.5, "S": 6.0},
    }

    def __init__(self, z: str, card: int):
        self.z = z
        self.card = card
        self.score = Z.score_table[card][z]

    def __str__(self):
        return f'Z{self.z}({self.score})'

    def __repr__(self):
        return f'Z{self.z}({self.score})'


class Spec:
    def __init__(self, spec: str):
        self.spec = spec

    def __str__(self):
        return self.spec

    def __repr__(self):
        return self.spec


class Reaction:
    def __init__(
            self,
            card: int,
            desc: str,
            pt: Part,
            dq: DQ,
            fq: FQ,
            det: List[Determination],
            cont: List[Content],
            p: bool,
            z: Optional[Z],
            spec: List[Spec]
    ):
        self.card = card
        self.desc = desc
        self.pt = pt
        self.dq = dq
        self.fq = fq
        self.det = det
        self.cont = cont
        self.p = p
        self.z = z
        self.spec = spec

    def __repr__(self):
        return f"""
        Card {self.card}: {self.desc}
        {self.pt}{self.dq} {'.'.join([str(d) for d in self.det])}{self.fq} {'.'.join([str(c) for c in self.cont])} {'P' if self.p else ''} {self.z if self.z else ''} {'.'.join([str(s) for s in self.spec])}
        """

    def __str__(self):
        return f"""
        Card {self.card}: {self.desc}
        {self.pt}{self.dq} {'.'.join([str(d) for d in self.det])}{self.fq} {'.'.join([str(c) for c in self.cont])} {'P' if self.p else ''} {self.z if self.z else ''} {'.'.join([str(s) for s in self.spec])}
        """

    def partIs(self, part: str):
        return self.pt.category == part

    def partContains(self, part: str):
        return part in self.pt.category

    def DQis(self, dq: str):
        return self.dq.dq == dq

    def FQis(self, fq: str):
        return self.fq.fq == fq

    def isBlend(self):
        return len([d for d in self.det if d.det != "(2)"]) >= 2

    def isColorShadeBlend(self):
        s = ''.join(self.simpDet())
        return 'C' in s and ("C'" in s or 'Y' in s or 'T' in s or 'V' in s)

    def simpDet(self) -> list:
        return [d.det for d in self.det]

    def detIs(self, det: str):
        return det in self.simpDet() and not self.isBlend()

    def detContains(self, det: str):
        return det in self.simpDet()

    def simpCont(self) -> list:
        return [c.cont for c in self.cont]

    def contContains(self, cont: str):
        return cont in self.simpCont()

    def simpSpec(self) -> list:
        return [s.spec for s in self.spec]

    def specContains(self, spec: str):
        return spec in self.simpSpec()

    def simpSpec6(self) -> list:
        return [s.spec for s in self.spec if s.spec in
                ['DV', 'DV2', 'INC', 'INC2', 'DR', 'DR2', 'FAB', 'FAB2', 'ALOG', 'CON']
                ]

    def WSum6(self) -> int:
        score = {
            'DV': 1,
            'DV2': 2,
            'INC': 2,
            'INC2': 4,
            'DR': 3,
            'DR2': 6,
            'FAB': 4,
            'FAB2': 7,
            'ALOG': 5,
            'CONT': 7
        }

        return sum([score[s] for s in self.simpSpec6()])

    def spec2Count(self):
        return sum([1 for s in self.spec if s.spec in ['DV2', 'INC2', 'DR2', 'FAB2']])

    def activeCount(self):
        return sum([1 for d in self.det if d.active()])

    def passiveCount(self):
        return sum([1 for d in self.det if d.passive()])

    def MActiveCount(self):
        return sum([1 for d in self.det if d.active() and d.det == 'M'])

    def MPassiveCount(self):
        return sum([1 for d in self.det if d.passive() and d.det == 'M'])


class Statistic:
    ZEst_table = {
        0: 0.0,
        1: 0.0,
        2: 2.5,
        3: 6.0,
        4: 10.0,
        5: 13.5,
        6: 17.0,
        7: 20.5,
        8: 24.0,
        9: 27.5,
        10: 31.0,
        11: 34.5,
        12: 38.0,
        13: 41.5,
        14: 45.5,
        15: 49.0,
        16: 52.5,
        17: 56.0,
        18: 59.5,
        19: 63.0,
        20: 66.5,
        21: 70.0,
        22: 73.5,
        23: 77.0,
        24: 81.0,
        25: 84.5,
        26: 88.0,
        27: 91.5,
        28: 95.0,
        29: 98.5,
        30: 102.5,
        31: 105.5,
        32: 109.5,
        33: 112.5,
        34: 116.5,
        35: 120.0,
        36: 123.5,
        37: 127.0,
        38: 130.5,
        39: 134.0,
        40: 137.5,
        41: 141.0,
        42: 144.5,
        43: 148.0,
        44: 152.0,
        45: 155.5,
        46: 159.0,
        47: 162.5,
        48: 166.0,
        49: 169.5,
        50: 173.0,
    }

    def __init__(self, path):
        self.reactions = self.readReactions(path)

        # 部位特征
        self.Zf = sum([1 for r in self.reactions if r.z])
        self.ZSum = sum([r.z.score for r in self.reactions if r.z])
        self.ZEst = Statistic.ZEst_table[self.Zf]

        self.W = sum([1 for r in self.reactions if r.partIs('W')])
        self.D = sum([1 for r in self.reactions if r.partIs('D')])
        self.W_D = self.W + self.D
        self.Dd = sum([1 for r in self.reactions if r.partIs('Dd')])
        self.S = sum([1 for r in self.reactions if r.partContains('S')])

        self.DQplus = sum([1 for r in self.reactions if r.DQis('+')])
        self.DQo = sum([1 for r in self.reactions if r.DQis('o')])
        self.DQvplus = sum([1 for r in self.reactions if r.DQis('v+')])
        self.DQv = sum([1 for r in self.reactions if r.DQis('v')])

        # 决定因子
        self.blends = [r.det for r in self.reactions if r.isBlend()]

        self.M = sum([1 for r in self.reactions if r.detIs('M')])
        self.FM = sum([1 for r in self.reactions if r.detIs('FM')])
        self.m = sum([1 for r in self.reactions if r.detIs('m')])
        self.FC = sum([1 for r in self.reactions if r.detIs('FC')])
        self.CF = sum([1 for r in self.reactions if r.detIs('CF')])
        self.C = sum([1 for r in self.reactions if r.detIs('C')])
        self.Cn = sum([1 for r in self.reactions if r.detIs('Cn')])
        self.FCp = sum([1 for r in self.reactions if r.detIs("FC'")])
        self.CpF = sum([1 for r in self.reactions if r.detIs("C'F")])
        self.Cp = sum([1 for r in self.reactions if r.detIs("C'")])
        self.FT = sum([1 for r in self.reactions if r.detIs('FT')])
        self.TF = sum([1 for r in self.reactions if r.detIs('TF')])
        self.T = sum([1 for r in self.reactions if r.detIs('T')])
        self.FV = sum([1 for r in self.reactions if r.detIs('FV')])
        self.VF = sum([1 for r in self.reactions if r.detIs('VF')])
        self.V = sum([1 for r in self.reactions if r.detIs('V')])
        self.FY = sum([1 for r in self.reactions if r.detIs('FY')])
        self.YF = sum([1 for r in self.reactions if r.detIs('YF')])
        self.Y = sum([1 for r in self.reactions if r.detIs('Y')])
        self.Fr = sum([1 for r in self.reactions if r.detIs('Fr')])
        self.rF = sum([1 for r in self.reactions if r.detIs('rF')])
        self.FD = sum([1 for r in self.reactions if r.detIs('FD')])
        self.F = sum([1 for r in self.reactions if r.detIs('F')])

        self.two = sum([1 for r in self.reactions if r.detContains('(2)')])

        # 形状质量
        self.FQplus = sum([1 for r in self.reactions if r.FQis('+')])
        self.FQo = sum([1 for r in self.reactions if r.FQis('o')])
        self.FQu = sum([1 for r in self.reactions if r.FQis('u')])
        self.FQminus = sum([1 for r in self.reactions if r.FQis('-')])
        self.FQnone = sum([1 for r in self.reactions if r.FQis('none')])

        self.MQualplus = sum([1 for r in self.reactions if r.detContains('M') and r.FQis('+')])
        self.MQualo = sum([1 for r in self.reactions if r.detContains('M') and r.FQis('o')])
        self.MQualu = sum([1 for r in self.reactions if r.detContains('M') and r.FQis('u')])
        self.MQualminus = sum([1 for r in self.reactions if r.detContains('M') and r.FQis('-')])
        self.MQualnone = sum([1 for r in self.reactions if r.detContains('M') and r.FQis('none')])

        self.W_Dplus = sum([1 for r in self.reactions if (r.partIs('W') or r.partIs('D')) and r.FQis('+')])
        self.W_Do = sum([1 for r in self.reactions if (r.partIs('W') or r.partIs('D')) and r.FQis('o')])
        self.W_Du = sum([1 for r in self.reactions if (r.partIs('W') or r.partIs('D')) and r.FQis('u')])
        self.W_Dminus = sum([1 for r in self.reactions if (r.partIs('W') or r.partIs('D')) and r.FQis('-')])
        self.W_Dnone = sum([1 for r in self.reactions if (r.partIs('W') or r.partIs('D')) and r.FQis('none')])

        # 内容

        self.H = sum([1 for r in self.reactions if r.contContains('H')])
        self.h = sum([1 for r in self.reactions if r.contContains('(H)')])
        self.Hd = sum([1 for r in self.reactions if r.contContains('Hd')])
        self.hd = sum([1 for r in self.reactions if r.contContains('(Hd)')])
        self.Hx = sum([1 for r in self.reactions if r.contContains('Hx')])
        self.A = sum([1 for r in self.reactions if r.contContains('A')])
        self.a = sum([1 for r in self.reactions if r.contContains('(A)')])
        self.Ad = sum([1 for r in self.reactions if r.contContains('Ad')])
        self.ad = sum([1 for r in self.reactions if r.contContains('(Ad)')])
        self.An = sum([1 for r in self.reactions if r.contContains('An')])
        self.Art = sum([1 for r in self.reactions if r.contContains('Art')])
        self.Ay = sum([1 for r in self.reactions if r.contContains('Ay')])
        self.Bl = sum([1 for r in self.reactions if r.contContains('Bl')])
        self.Bt = sum([1 for r in self.reactions if r.contContains('Bt')])
        self.Cg = sum([1 for r in self.reactions if r.contContains('Cg')])
        self.Cl = sum([1 for r in self.reactions if r.contContains('Cl')])
        self.Ex = sum([1 for r in self.reactions if r.contContains('Ex')])
        self.Fd = sum([1 for r in self.reactions if r.contContains('Fd')])
        self.Fi = sum([1 for r in self.reactions if r.contContains('Fi')])
        self.Ge = sum([1 for r in self.reactions if r.contContains('Ge')])
        self.Hh = sum([1 for r in self.reactions if r.contContains('Hh')])
        self.Ls = sum([1 for r in self.reactions if r.contContains('Ls')])
        self.Na = sum([1 for r in self.reactions if r.contContains('Na')])
        self.Sc = sum([1 for r in self.reactions if r.contContains('Sc')])
        self.Sx = sum([1 for r in self.reactions if r.contContains('Sx')])
        self.Xy = sum([1 for r in self.reactions if r.contContains('Xy')])
        self.Id = sum([1 for r in self.reactions if r.contContains('Id')])

        #  部位序列

        self.part_seq = {
            1: [r.pt.category for r in self.reactions if r.card == 1],
            2: [r.pt.category for r in self.reactions if r.card == 2],
            3: [r.pt.category for r in self.reactions if r.card == 3],
            4: [r.pt.category for r in self.reactions if r.card == 4],
            5: [r.pt.category for r in self.reactions if r.card == 5],
            6: [r.pt.category for r in self.reactions if r.card == 6],
            7: [r.pt.category for r in self.reactions if r.card == 7],
            8: [r.pt.category for r in self.reactions if r.card == 8],
            9: [r.pt.category for r in self.reactions if r.card == 9],
            10: [r.pt.category for r in self.reactions if r.card == 10],
        }

        # 特殊分数
        self.DV = sum([1 for r in self.reactions if r.specContains('DV')])
        self.DV2 = sum([1 for r in self.reactions if r.specContains('DV2')])
        self.INC = sum([1 for r in self.reactions if r.specContains('INC')])
        self.INC2 = sum([1 for r in self.reactions if r.specContains('INC2')])
        self.DR = sum([1 for r in self.reactions if r.specContains('DR')])
        self.DR2 = sum([1 for r in self.reactions if r.specContains('DR2')])
        self.FAB = sum([1 for r in self.reactions if r.specContains('FAB')])
        self.FAB2 = sum([1 for r in self.reactions if r.specContains('FAB2')])
        self.ALOG = sum([1 for r in self.reactions if r.specContains('ALOG')])
        self.CON = sum([1 for r in self.reactions if r.specContains('CONT')])
        self.AB = sum([1 for r in self.reactions if r.specContains('AB')])
        self.AG = sum([1 for r in self.reactions if r.specContains('AG')])
        self.COP = sum([1 for r in self.reactions if r.specContains('COP')])
        self.CP = sum([1 for r in self.reactions if r.specContains('CP')])
        self.GHR = sum([1 for r in self.reactions if r.specContains('GHR')])
        self.PHR = sum([1 for r in self.reactions if r.specContains('PHR')])
        self.MOR = sum([1 for r in self.reactions if r.specContains('MOR')])
        self.PER = sum([1 for r in self.reactions if r.specContains('PER')])
        self.PSV = sum([1 for r in self.reactions if r.specContains('PSV')])

        self.Sum6 = sum([len(r.simpSpec6()) for r in self.reactions])
        self.WSum6 = sum([r.WSum6() for r in self.reactions])

        # ----------------下半部分-----------------

        # 核心部分
        self.SumCp = self.Cp + self.CpF + self.FCp
        self.SumT = self.T + self.TF + self.FT
        self.SumV = self.V + self.VF + self.FV
        self.SumY = self.Y + self.YF + self.FY

        self.R = len(self.reactions)
        self.L = self.F / (self.R - self.F)

        self.WSumC = 0.5 * self.FC + 1.0 * self.CF + 1.5 * self.C
        self.EB = Ratio(self.M, self.WSumC)
        self.EA = self.M + self.WSumC
        # self.RBPer = self.EB.abs_value()  # TODO: check this
        self.eb = Ratio(self.FM + self.m, self.SumCp + self.SumT + self.SumV + self.SumY)
        self.es = self.FM + self.m + self.SumCp + self.SumT + self.SumV + self.SumY
        self.Dscore = self.DConvert(self.EA - self.es)
        self.Adjes = self.FM + max(self.m, 1) + self.SumCp + self.SumT + self.SumV + max(self.SumY, 1)
        self.AdjD = self.DConvert(self.EA - self.Adjes)

        # 思维部分
        self.P = sum([1 for r in self.reactions if r.p])
        self.Lv2 = sum([r.spec2Count() for r in self.reactions])
        self.APR = Ratio(
            sum([r.activeCount() for r in self.reactions]), sum([r.passiveCount() for r in self.reactions]))
        self.MAPR = Ratio(
            sum([r.MActiveCount() for r in self.reactions]), sum([r.MPassiveCount() for r in self.reactions]))
        self.Intel = 2 * self.AB + self.Art + self.Ay

        # 情绪部分
        self.FCR = Ratio(self.FC, self.CF + self.C)
        self.CpCR = Ratio(self.Cp, self.WSumC)
        self.Afr = (sum([1 for r in self.reactions if r.card in (8, 9, 10)]) /
                    (self.R - sum([1 for r in self.reactions if r.card in (8, 9, 10)])))
        self.ComR = Ratio(len(self.blends), self.R)

        # 调节部分
        self.Sminus = sum([1 for r in self.reactions if r.FQis('-') and r.partContains('S')])
        self.XA = sum([1 for r in self.reactions if r.fq.fq in ('+', 'o', 'u')]) / self.R
        self.WDA = sum(
            [1 for r in self.reactions if r.pt.category in ('W', 'D') and r.fq.fq in ('+', 'o', 'u')]) / self.R
        self.Xminus = sum([1 for r in self.reactions if r.fq.fq == '-']) / self.R
        self.Xplus = sum([1 for r in self.reactions if r.fq.fq in ('+', 'o')]) / self.R
        self.Xu = sum([1 for r in self.reactions if r.fq.fq == 'u']) / self.R

        # 加工部分
        self.EcoI = TriRatio(self.W, self.D, self.Dd)
        self.AspR = Ratio(self.W, sum([1 for r in self.reactions if r.detContains('M')]))
        self.Zd = self.ZSum - self.ZEst

        # 人际交往部分
        self.GHR_PHR = Ratio(self.GHR, self.PHR)
        self.HCont = self.H + self.h + self.Hd + self.hd
        self.IsoI = (self.Bt + 2 * self.Cl + self.Ge + self.Ls + 2 * self.Na) / self.R

        # 自我知觉部分
        self.Fr_rF = self.Fr + self.rF
        self.An_Xy = self.An + self.Xy
        self.H_hd = Ratio(self.H, self.h + self.Hd + self.hd)
        self.EgoI = (3 * self.Fr_rF + self.two) / self.R

        # 特殊指数
        # 自杀指数
        self.SCON1 = self.FV + self.VF + self.V + self.FD > 2
        self.SCON2 = sum([1 for r in self.reactions if r.isColorShadeBlend()]) > 0
        self.SCON3 = self.EgoI < 0.31 or self.EgoI > 0.44
        self.SCON4 = self.MOR > 3
        self.SCON5 = self.Zd > 3.5 or self.Zd < -3.5
        self.SCON6 = self.es > self.EA
        self.SCON7 = self.CF + self.C > self.FC
        self.SCON8 = self.Xplus < 0.7
        self.SCON9 = self.S > 3
        self.SCON10 = self.P < 3 or self.P > 8
        self.SCON11 = self.H < 2
        self.SCON12 = self.R < 17

        self.SCON = [self.SCON1, self.SCON2, self.SCON3, self.SCON4, self.SCON5, self.SCON6, self.SCON7, self.SCON8,
                     self.SCON9,
                     self.SCON10, self.SCON11, self.SCON12]

        # 知觉思维指数
        self.PTI1 = self.XA < 0.7 or self.WDA < 0.75
        self.PTI2 = self.Xminus > 0.29
        self.PTI3 = self.Lv2 > 2 and self.FAB2 > 0
        self.PTI4 = self.R < 17 and self.WSum6 > 12 or self.R > 16 and self.WSum6 > 17
        self.PTI5 = self.MQualminus > 1 or self.Xminus > 0.4

        self.PTI = [self.PTI1, self.PTI2, self.PTI3, self.PTI4, self.PTI5]

        # 抑郁指数
        self.DEPI1 = self.SumV > 0 or self.FD > 2
        self.DEPI2 = sum([1 for r in self.reactions if r.isColorShadeBlend()]) > 0 or self.S > 2
        self.DEPI3 = self.EgoI > 0.44 and self.Fr_rF == 0 or self.EgoI < 0.33
        self.DEPI4 = self.Afr < 0.46 or len(self.blends) < 4
        self.DEPI5 = self.SumCp + self.SumT + self.SumV + self.SumY > self.FM + self.m or self.SumCp > 2
        self.DEPI6 = self.MOR > 2 or self.Intel > 3
        self.DEPI7 = self.COP < 2 or self.IsoI > 0.24

        self.DEPI = [self.DEPI1, self.DEPI2, self.DEPI3, self.DEPI4, self.DEPI5, self.DEPI6, self.DEPI7]

        # 应对缺陷指数
        self.CDI1 = self.EA < 6 or self.AdjD < 0
        self.CDI2 = self.COP < 2 or self.AG < 2
        self.CDI3 = self.WSumC < 2.5 or self.Afr < 0.46
        self.CDI4 = self.P > sum([r.activeCount() for r in self.reactions]) + 1 or self.H < 2
        self.CDI5 = self.MQualminus > 1 or self.Xminus > 0.4

        self.CDI = [self.CDI1, self.CDI2, self.CDI3, self.CDI4, self.CDI5]

        # 高警觉指数
        self.HVI1 = self.SumT == 0
        self.HVI2 = self.Zf > 12
        self.HVI3 = self.Zd > 3.5
        self.HVI4 = self.S > 3
        self.HVI5 = self.HCont > 6
        self.HVI6 = self.h + self.a + self.hd + self.ad > 3
        self.HVI7 = (self.H + self.A) / (self.Hd + self.Ad) < 4
        self.HVI8 = self.Cg > 3

        self.HVI = self.HVI1 and sum([self.HVI2, self.HVI3, self.HVI4, self.HVI5, self.HVI6, self.HVI7, self.HVI8]) >= 4

        # 强迫指数
        self.OBS1 = self.Dd > 3
        self.OBS2 = self.Zf > 12
        self.OBS3 = self.Zd > 3
        self.OBS4 = self.P > 7
        self.OBS5 = self.FQplus > 1

        self.OBS = sum([self.OBS1, self.OBS2, self.OBS3, self.OBS4, self.OBS5]) == 5 or \
                   sum([self.OBS1, self.OBS2, self.OBS3, self.OBS4, self.OBS5]) >= 2 and self.FQplus > 3 or \
                   sum([self.OBS1, self.OBS2, self.OBS3, self.OBS4, self.OBS5]) >= 3 and self.Xplus > 0.89 or \
                   self.FQplus > 3 and self.Xplus > 0.89

    def DConvert(self, EA_es):
        if EA_es < 0:
            return - self.DConvert(-EA_es)

        if EA_es < 1:
            return 0
        else:
            return (EA_es - 0.1) // 2.5

    def readReactions(self, path) -> List[Reaction]:
        dataframe = pandas.read_excel(path)

        reactions: List[Reaction] = []
        for index, row in dataframe.iterrows():
            reactions.append(
                Reaction(card=row['Card'], desc=row['Desc'], pt=Part(row['Pt']), dq=DQ(row['DQ']), fq=FQ(row['FQ']),
                         det=[Determination(det) for det in row['Det'].split('.')],
                         cont=[Content(cont) for cont in row['Cont'].split('.')], p=not pandas.isna(row['P']),
                         z=Z(row['Z'], row['Card']) if not pandas.isna(row['Z']) else None,
                         spec=[Spec(spec) for spec in row['Spec'].split('.')] if not pandas.isna(row['Spec']) else [])
            )
        return reactions

    def __repr__(self):
        return f"""
部位特征
Zf = {self.Zf}
ZSum = {self.ZSum}
ZEst = {self.ZEst}
W = {self.W}
D = {self.D}
W+D = {self.W_D}
Dd = {self.Dd}
S = {self.S}

决定因子
Blends = {self.blends}
M = {self.M}
FM = {self.FM}
m = {self.m}
FC = {self.FC}
CF = {self.CF}
C = {self.C}
Cn = {self.Cn}
FC' = {self.FCp}
C'F = {self.CpF}
C' = {self.Cp}
FT = {self.FT}
TF = {self.TF}
T = {self.T}
FV = {self.FV}
VF = {self.VF}
V = {self.V}
FY = {self.FY}
YF = {self.YF}
Y = {self.Y}
Fr = {self.Fr}
rF = {self.rF}
FD = {self.FD}
F = {self.F}
(2) = {self.two}

形状质量
FQ+ = {self.FQplus}
FQo = {self.FQo}
FQu = {self.FQu}
FQ- = {self.FQminus}
FQnone = {self.FQnone}

MQual+ = {self.MQualplus}
MQualo = {self.MQualo}
MQualu = {self.MQualu}
MQual- = {self.MQualminus}
MQualnone = {self.MQualnone}

W+D+ = {self.W_Dplus}
W+Do = {self.W_Do}
W+Du = {self.W_Du}
W+D- = {self.W_Dminus}
W+Dnone = {self.W_Dnone}

内容
H = {self.H}
(H) = {self.h}
Hd = {self.Hd}
(Hd) = {self.hd}
Hx = {self.Hx}
A = {self.A}
(A) = {self.a}
Ad = {self.Ad}
(Ad) = {self.ad}
An = {self.An}
Art = {self.Art}
Ay = {self.Ay}
Bl = {self.Bl}
Bt = {self.Bt}
Cg = {self.Cg}
Cl = {self.Cl}
Ex = {self.Ex}
Fd = {self.Fd}
Fi = {self.Fi}
Ge = {self.Ge}
Hh = {self.Hh}
Ls = {self.Ls}
Na = {self.Na}
Sc = {self.Sc}
Sx = {self.Sx}
Id = {self.Id}

部位序列
1 = {self.part_seq[1]}
2 = {self.part_seq[2]}
3 = {self.part_seq[3]}
4 = {self.part_seq[4]}
5 = {self.part_seq[5]}
6 = {self.part_seq[6]}
7 = {self.part_seq[7]}
8 = {self.part_seq[8]}
9 = {self.part_seq[9]}
10 = {self.part_seq[10]}

特殊分数
DV = {self.DV}
DV2 = {self.DV2}
INC = {self.INC}
INC2 = {self.INC2}
DR = {self.DR}
DR2 = {self.DR2}
FAB = {self.FAB}
FAB2 = {self.FAB2}
ALOG = {self.ALOG}
CON = {self.CON}
AB = {self.AB}
AG = {self.AG}
COP = {self.COP}
CP = {self.CP}
GHR = {self.GHR}
PHR = {self.PHR}
MOR = {self.MOR}
PER = {self.PER}
PSV = {self.PSV}

Sum6 = {self.Sum6}
WSum6 = {self.WSum6}

------------
核心部分
R = {self.R}
L = {self.L}

EB = {self.EB}
EA = {self.EA}
EBPer = ?
eb = {self.eb}
es = {self.es}
D = {self.Dscore}
Adjes = {self.Adjes}
AdjD = {self.AdjD}

FM = {self.FM}
m = {self.m}
SumC' = {self.SumCp}
SumT = {self.SumT}
SumV = {self.SumV}
SumY = {self.SumY}

思维部分
a:p = {self.APR}
Ma:Mp = {self.MAPR}
2AB+(Art+Ay) = {self.Intel}
MOR = {self.MOR}

Sum6 = {self.Sum6}
Lv2 = {self.Lv2}
WSum6 = {self.WSum6}
M- = {self.MQualminus}
Mnone = {self.MQualnone}

情绪部分
FC:CF+C = {self.FCR}
PureC = {self.C}
SumC':WSumC = {self.CpCR}
Afr = {self.Afr}
S = {self.S}
Blends:R = {self.ComR}
CP = {self.Cp}

调节部分
XA% = {self.XA}
WDA% = {self.WDA}
X-% = {self.Xminus}
S- = {self.Sminus}
P = {self.P}
X+% = {self.Xplus}
Xu% = {self.Xu}

加工部分
Zf = {self.Zf}
W:D:Dd = {self.EcoI}
W:M = {self.AspR}
Zd = {self.Zd}
PSV = {self.PSV}
DQ+ = {self.DQplus}
DQv = {self.DQv}

人际交往部分
COP = {self.COP}
GHR:PHR = {self.GHR_PHR}
a:p = {self.APR}
Food = {self.Fd}
SumT = {self.SumT}
Hum Cont = {self.HCont}
PureH = {self.H}
PER = {self.PER}
Iso Index = {self.IsoI}

自我知觉部分
3r+(2)/R = {self.EgoI}
Fr+rF = {self.Fr_rF}
SumV = {self.SumV}
FD = {self.FD}
An+Xy = {self.An_Xy}
MOR = {self.MOR}
H:(H)+Hd+(Hd) = {self.H_hd}

特殊指数
PTI = {sum(self.PTI)} ({','.join([str(i + 1) for i, _ in enumerate(self.PTI) if _])})
DEPI = {sum(self.DEPI)} ({','.join([str(i + 1) for i, _ in enumerate(self.DEPI) if _])})
CDI = {sum(self.CDI)} ({','.join([str(i + 1) for i, _ in enumerate(self.CDI) if _])})
S-CON = {sum(self.SCON)} ({','.join([str(i + 1) for i, _ in enumerate(self.SCON) if _])})
HVI = {self.HVI}
OBS = {self.OBS}
        """


if __name__ == '__main__':
    statistic = Statistic('data/hjh.xlsx')
    print(statistic)
