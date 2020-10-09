import numpy as np

_test_values = {
    'x': np.array([2.5, 2.7, 2.9, 3.1, 3.3000000000000003, 3.5, 3.7, 3.9, 4.1, 4.3, 4.5, 4.7, 4.9, 5.1000000000000005, 5.3, 5.5, 5.7, 5.9, 6.1000000000000005, 6.3, 6.5, 6.7, 6.9, 7.1000000000000005, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3, 8.5, 8.700000000000001, 8.9, 9.1, 9.3, 9.5, 9.700000000000001, 9.9, 10.1, 10.3, 10.5, 10.700000000000001, 10.9, 11.1, 11.3, 11.5, 11.700000000000001, 11.9, 12.1, 12.3, 12.5, 12.700000000000001, 12.9, 13.1, 13.3, 13.5, 13.700000000000001, 13.9, 14.1, 14.3, 14.5, 14.700000000000001, 14.9, 15.1, 15.3, 15.5, 15.700000000000001, 15.9, 16.1, 16.3, 16.5, 16.7, 16.9, 17.1, 17.3, 17.5, 17.7, 17.900000000000002, 18.1, 18.3, 18.5, 18.7, 18.900000000000002, 19.1, 19.3, 19.5, 19.7, 19.900000000000002, 20.1, 20.3, 20.5, 20.7, 20.900000000000002, 21.1, 21.3, 21.5, 21.7, 21.900000000000002, 22.1, 22.3, 22.5]),
    'dec': np.array([0.44727683672754365, 0.4474826620662529, 0.4480840464104767, 0.44906806102014235, 0.450424607833821, 0.4521461589927827, 0.4542275151649557, 0.45666559778272325, 0.4594592793643863, 0.4626092445283497, 0.46611787552419437, 0.46998917603669815, 0.4742287187169857, 0.4788436075892289, 0.4838424525429636, 0.4892353532452736, 0.49503390935182656, 0.5012512452966373, 0.5079020425507385, 0.5150025777243382, 0.5225707646117943, 0.5306264432413383, 0.5391918172130394, 0.5482919961439691, 0.5579556738630922, 0.5682159815868888, 0.5791109521049392, 0.5906838604572003, 0.602983596129938, 0.6160650581751314, 0.6299895595341204, 0.6448255683241987, 0.6606496674060534, 0.6775476686751006, 0.6956159086397659, 0.7149627562960101, 0.7357104297105456, 0.757997153618676, 0.7819797081574964, 0.807836445199551, 0.8357708627397145, 0.866016682351557, 0.8988445447604376, 0.93457066108687, 0.9735681595112573, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]),
    'kh0s': np.array([1012.9407801051351, 1168.777823198233, 1324.6148662913306, 1480.4519093844283, 1386.0642457837225, 1208.2683466184158, 1030.4724474531088, 852.6765482878018, 674.8806491224949, 604.0013576474807, 568.7609354025643, 533.520513157648, 498.28009091273145, 463.03966866781514, 525.9500204392048, 621.5772968826966, 717.2045733261884, 812.8318497696802, 908.4591262131721, 2067.541406105329, 3581.1086871470407, 5094.6759681887515, 6608.243249230463, 8121.810530272175, 7415.098394222426, 5968.2931191421885, 4521.487844061952, 3074.682568981715, 1627.8772939014782, 1190.205416623534, 1088.9113386130202, 987.6172606025067, 886.3231825919931, 785.0291045814796, 816.6835039597652, 892.6540624676503, 968.6246209755355, 1044.5951794834207, 1120.565737991306, 2509.2862970095703, 4335.5901895312945, 6161.894082053018, 7988.197974574741, 9814.501867096464, 8863.231825919933, 6986.103806843983, 5108.975787768033, 3231.8477686920833, 1354.7197496161336, 1337.0109947191906, 1939.10866121525, 2541.2063277113093, 3143.3039942073688, 3745.401660703428, 31441.894319522165, 68169.85197578178, 104897.8096320414, 141625.76728830102, 178353.72494456064, 219172.4049820141, 261354.6591465321, 303536.91331105016, 345719.1674755682, 387901.4216400863, 382137.2219211313, 360390.87090768537, 338644.5198942394, 316898.1688807935, 295151.8178673475, 259273.88044614103, 218685.41422234793, 178096.9479985548, 137508.48177476172, 96920.01555096859, 97663.78325664022, 112184.96227213342, 126706.14128762661, 141227.3203031198, 155748.499318613, 203765.78822167375, 262948.44708725705, 322131.10595284024, 381313.76481842354, 440496.4236840068, 434811.91336208815, 407505.0133110021, 380198.1132599161, 352891.2132088301, 325584.3131577441, 390478.04547759145, 486105.32192108326, 581732.5983645751, 677359.8748080668, 772987.1512515586, 711520.0630042697, 597688.1865267206, 483856.3100491715, 370024.4335716223, 256192.5570940733, 359543.6467918264, 535289.0585480138]),
    'y': np.array([49.98586183063796, 49.93988914081713, 49.80592805172261, 49.58789399810607, 49.28965539285511, 48.91502821012051, 48.46777947640144, 47.9516337116514, 47.37027935013679, 46.72737512595333, 46.02655640883777, 45.27143780033758, 44.46561449268402, 43.61266362130758, 42.7161456082459, 41.77960549381545, 40.80657102723699, 39.80054974797933, 38.7650261496195, 37.70345893091541, 36.61927833850935, 35.51585075801561, 34.39643356525719, 33.26413140657767, 32.121853970775206, 30.972275311301367, 29.81785807482466, 28.660897821791394, 27.503565911444497, 26.347950898571995, 25.196098391535756, 24.050023265441155, 22.911712899058365, 21.78313030626413, 20.66621715862293, 19.562896695845584, 18.47507348052071, 17.40463221300435, 16.353436648692, 15.323328619266565, 14.316127159381676, 13.333601887876604, 12.377439895271442, 11.449215075633337, 10.550359935225872, 9.682139907140662, 8.845675587561903, 8.041980024606218, 7.2719944107149574, 6.536618613591483, 5.836736837063701, 5.17321938913414, 4.546918582116223, 3.9586658258803835, 3.409269805511954, 2.8995156315434425, 2.4300179765586405, 2.0010772351069295, 1.6125885059135927, 1.263996276122081, 0.9542877320697651, 0.6820095783733655, 0.44531196247624605, 0.2420158785241629, 0.06969753609026741, -0.07421612144477807, -0.19234049870869052, -0.2872484729853555, -0.36140935703483157, -0.4171477285785792, -0.4566185593904266, -0.4818048543397511, -0.49453084787358226, -0.4964843400433345, -0.48924500764897516, -0.47431601801004347, -0.45312456598953416, -0.42701324093796006, -0.39723334466751853, -0.3649402927515855, -0.33119113005699247, -0.2969246655651977, -0.2629412414976576, -0.22988911900475528, -0.19825714121535867, -0.16837313971025758, -0.1404278810933509, -0.11450303768629934, -0.09059539122641358, -0.06863747627009964, -0.04851492813432661, -0.030070767954661626, -0.013110519394536037, 0.0025881079269908986, 0.01726152441979551, 0.03114295958742044, 0.0444461147196426, 0.057355095258996874, 0.07001981292141926, 0.08255643526213516]),
    't': np.array([0.0, -0.44983444728837085, -0.8799878567776531, -1.29068164716875, -1.6821644699638938, -2.0546897911341766, -2.408486246172785, -2.7437503156616216, -3.060646464245167, -3.3593073532475515, -3.639843314039375, -3.902354790384379, -4.146935447574993, -4.37367221109529, -4.582645318730325, -4.773936452522278, -4.947639364590302, -5.1038621940437245, -5.242727042659805, -5.36436952777537, -5.469020432249501, -5.5571119331304075, -5.629298378594854, -5.686448986204962, -5.729640238190754, -5.7599897398763655, -5.778443723774931, -5.785730408450407, -5.782367308048499, -5.768668799771852, -5.7448190828270995, -5.710963731193477, -5.667232397942561, -5.613739351088585, -5.550584026046366, -5.477859195255554, -5.395661207103082, -5.304092079571774, -5.203258984344465, -5.093273723275811, -4.974316828474903, -4.846718160275585, -4.710967030608169, -4.567699900113924, -4.4176879212316855, -4.261710869159923, -4.100399706336111, -3.9342029421173645, -3.763403527536837, -3.5881439341281407, -3.408498061143359, -3.2245456373686965, -3.03638390813439, -2.844121941510671, -2.6478754858423525, -2.448129572383284, -2.2460959910912823, -2.0435736766126196, -1.842702397462121, -1.645751934609569, -1.454966744371789, -1.2724394239837977, -1.0999842496230066, -0.9390360659649466, -0.7905799999223524, -0.6550950869973948, -0.5325808788514436, -0.4226721458153526, -0.3247481389830592, -0.23802300588898762, -0.16164281440292985, -0.09478072120788911, -0.036698714258958515, 0.013214600561517742, 0.05542080508322764, 0.09030110414860251, 0.11825694268020853, 0.13972805330503907, 0.15518237046593636, 0.16510553652631516, 0.17003906796596954, 0.17062472139833723, 0.16758886640110604, 0.16171025070574727, 0.15378994823624426, 0.14457315030501947, 0.1346752550598956, 0.12458122466734325, 0.11466390354049925, 0.10520115773021742, 0.09641677078859504, 0.08851102184947643, 0.0816471897041313, 0.07593010953582886, 0.07138712915107386, 0.06796147574961772, 0.06553033917894108, 0.06393424550444166, 0.06300335000784571, 0.06258198667957497]),
    'm': np.array([2313.322671572006, 2213.8105240261125, 2115.34325826886, 2018.0585615149384, 1922.0370559950559, 1827.2283868649583, 1733.489194357425, 1640.658042040003, 1548.5743779875706, 1457.1020175806493, 1366.1599101846236, 1275.7061284717872, 1185.7066641208157, 1096.1277371688286, 1006.9561565396575, 918.2259206286424, 830.0035882334279, 742.3604793966587, 655.3657218781583, 569.2927277720258, 484.8875607938089, 403.2157962814811, 325.37690950810384, 252.43287513895964, 185.00856934404393, 122.77631919948963, 64.75653333825437, 9.870672748298302, -42.922375074253225, -94.46114001848176, -145.17028516307636, -195.18703377413473, -244.5901431597921, -293.45563274012187, -341.8375795445516, -389.7437496970964, -437.150883921364, -484.0317537434644, -530.3617455982849, -575.9563045712888, -620.2668547334245, -662.5165898906647, -701.9341869139157, -737.8106116056482, -769.785323450979, -798.2110024306423, -823.9210234602006, -847.7908887450934, -870.5905063575824, -892.8457938196301, -914.7145948485636, -936.1381770503967, -957.0427307523642, -977.3817073935058, -996.2092856807984, -1010.7681224998478, -1017.7527936504275, -1014.828757036581, -1000.8114911468397, -975.4376298949322, -939.1529194507513, -893.0395762477705, -838.7523271406602, -778.3770865587991, -714.3184108726512, -649.0557398232152, -584.7130153568885, -522.8507452848468, -464.52710236050825, -410.3287122647429, -360.3586968503873, -314.325432656039, -271.68690799230876, -231.74769949068417, -193.92871343289963, -158.07866168828002, -124.3447842720295, -92.89435076473474, -63.84285759837744, -37.375417199826494, -13.884770635892316, 6.164041888194675, 22.426387913628293, 34.7143315879468, 43.11229175064536, 48.08737824211006, 50.294256939295245, 50.34312718342342, 48.75498657316156, 45.90483176368866, 41.98785037274226, 37.156255951045914, 31.650159564463177, 25.811526664330877, 20.046919059340684, 14.734093405330041, 10.131417872166958, 6.3572186570347915, 3.401916054454671, 1.3144388346260831]),
    'q': np.array([-500.0, -494.9485332578653, -489.37990627793494, -483.26550568451046, -477.07543662495016, -471.3696540940768, -466.4258620623887, -462.28704092463613, -458.89006114838423, -456.0361695073676, -453.48972277215546, -451.1331151595199, -448.94597825739623, -446.87626895289543, -444.75454135046573, -442.38142076557426, -439.66360307995944, -436.59466588817384, -432.6693790615821, -426.19540271087345, -415.19232872636167, -398.7766282142627, -376.9573028563038, -350.9208504101498, -324.141389848675, -300.6300900144739, -282.2641161279783, -269.197271031269, -260.82953191695015, -255.61977522205785, -251.81473438913247, -248.5496449917893, -245.67149741496786, -243.1185909618988, -240.72029239243628, -238.28326094203115, -235.72001011592002, -233.02715419230194, -229.81137706956105, -224.76277283784896, -216.40071329843968, -204.16833045122831, -188.23505428745895, -169.6278413426584, -151.00097706248522, -135.33925002305358, -123.94971578612775, -116.67370724345476, -112.63726268634171, -110.31022122745306, -108.23095807691664, -105.82033975950122, -103.10882585777283, -97.91638732108562, -83.4660377658546, -53.858769924072924, -10.151586341833173, 42.3532562589696, 98.47781785412192, 154.14642924022107, 205.99513411790429, 251.00148077522755, 286.65622422242853, 311.08479067002264, 323.30336683895973, 324.0134887894067, 315.51248634592116, 300.46478249095065, 281.30508255025967, 260.42101377530247, 240.00819902175962, 221.6794721451962, 206.4443329133872, 194.39548639852293, 184.17259450601043, 173.95982290217532, 162.9607773088632, 151.25481668413013, 138.79733391227063, 124.89521740621282, 108.84864772005292, 90.77789637380152, 71.37572424938033, 51.71475959254266, 33.43261663540816, 17.95491297162471, 5.63937235328339, -3.848175915334206, -11.095738549336902, -16.917840501048268, -21.871439531606867, -25.844227020697698, -28.361823216787595, -29.008101262806235, -27.69358314750209, -24.78875296793432, -20.942186870738123, -16.823754544280717, -12.606949556021771, -7.232774615359034]),
}

_YOUNG_MODULES = {
    'concrete': 2.05e4,
    'steel': 2.05e5
}


def get_results(mode, dec_mode, condition, material, diameter, length, level, force, **kwargs) -> dict:

    kh0s = _test_values.get('kh0s') / 1e6
    dec = _test_values.get('dec')

    diameter = float(diameter)  # mm
    length = float(length) * 1e3  # to mm
    level = float(level) * 1e3  # to mm
    force = float(force) * 1e3  # to N

    k0 = top_condition_to_stiffness(condition)
    stiffness = pile_stiffness(diameter, diameter, 0, material)

    div_num = 100
    div_size = length / div_num

    x = np.linspace(-level, length - level, div_num + 1)

    # solve y
    if mode == 'liner':
        y = deformation_analysis_by_FDM(div_num, div_size, stiffness, diameter, kh0s, k0, force)
    elif mode == 'non_liner':
        # TODO:
        y = deformation_analysis_by_FDM(div_num, div_size, stiffness, diameter, kh0s, k0, force)

    # solve t
    t = np.gradient(y, div_size)

    # solve m
    m = -np.gradient(t, div_size) * stiffness

    # solve q
    q = np.gradient(m, div_size)
    q[2] = -force

    return dict(
        x=x/1e3,
        dec=dec,
        kh0s=kh0s*1e6,
        y=y[2:-3],
        t=t[2:-3],
        m=m[2:-3]/1e6,
        q=q[2:-3]/1e3
    )


def top_condition_to_stiffness(condition: str) -> float:
    return np.inf if condition == "fix" else 10e-10


def pile_stiffness(diameter: float, thickness: float, thickness_margin: float, material: str) -> float:
    sec1 = np.pi * (diameter - thickness_margin * 2) ** 4 / 64
    sec2 = np.pi * (diameter - thickness) ** 4 / 64
    return (sec1 - sec2) * _YOUNG_MODULES.get(material)


def deformation_analysis_by_FDM(div_num: int, div_size: float, stiffness: float, diameter: float, khs: np.ndarray, k0: float, force: float) -> np.ndarray:
    left = _left_matrix(div_num, div_size, stiffness, diameter, khs, k0)
    right = _right_matrix(div_num, div_size, stiffness, force)
    ans = -np.linalg.solve(left, right)  # 連立方程式を解く
    return ans


def _left_matrix(n, h, ei, b, khs, k0):
    left = np.zeros((n + 5, n + 5))
    # head row
    left[0, 0:5] = [-1, 2, 0, -2, 1]
    left[1, 0:5] = [0, ei / k0 - h, -2 * ei / k0, ei / k0 + h, 0]
    # general row
    c1s = 6 + h ** 4 * khs * b / ei
    for i in range(2, n + 3):
        left[i, i - 2:i + 3] = [1, -4, c1s[i - 2], -4, 1]
    # tail row
    left[-1, -5:] = [-1, 2, 0, -2, 1]
    left[-2, -5:] = [0, 1, -2, 1, 0]
    return left


def _right_matrix(n, h, ei, force):
    right = np.zeros(n + 5)
    right[0] = -2 * force * h ** 3 / ei
    return right
