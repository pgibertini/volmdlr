#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 15:15:37 2021

@author: dasilva
"""


import volmdlr.cloud
import volmdlr.core
import volmdlr as vm
import volmdlr.wires as vmw
import volmdlr.faces as vmf
import volmdlr.edges as vme
import matplotlib.pyplot as plt
# import cv2
import numpy as np
from scipy.spatial import Delaunay

'''
circle with Triangle
'''
polygons_points=[[vm.Point3D(-0.02785286331176758, 0.14365164184570312, 0.16285931396484374),
vm.Point3D(-0.039570194244384765, 0.14255133056640626, 0.16285931396484374),
vm.Point3D(-0.04901511764526367, 0.14049978637695312, 0.16285931396484374),
vm.Point3D(-0.05265781402587891, 0.138816650390625, 0.16285931396484374),
vm.Point3D(-0.05629143524169922, 0.1368720245361328, 0.16285931396484374),
vm.Point3D(-0.06060961151123047, 0.1323123321533203, 0.16285931396484374),
vm.Point3D(-0.06237499237060547, 0.12723016357421876, 0.16285931396484374),
vm.Point3D(-0.06580715942382813, 0.11276873016357422, 0.16285931396484374),
vm.Point3D(-0.06730508422851562, 0.09772169494628906, 0.16285931396484374),
vm.Point3D(-0.06716297912597656, 0.09380774688720703, 0.16285931396484374),
vm.Point3D(-0.06691159057617188, 0.08986341857910156, 0.16285931396484374),
vm.Point3D(-0.06653813171386719, 0.08590738677978516, 0.16285931396484374),
vm.Point3D(-0.06329383087158204, 0.07401349639892578, 0.16285931396484374),
vm.Point3D(-0.05981048965454101, 0.06631576538085937, 0.16285931396484374),
vm.Point3D(-0.01858608627319336, -0.0005872868895530701, 0.16285931396484374),
vm.Point3D(0.004057138919830322, -0.026433467864990234, 0.16285931396484374),
vm.Point3D(0.004993902683258057, -0.027147762298583983, 0.16285931396484374),
vm.Point3D(0.0060211563110351566, -0.02774390983581543, 0.16285931396484374),
vm.Point3D(0.007130794048309326, -0.02821550941467285, 0.16285931396484374),
vm.Point3D(0.008299141883850098, -0.028550893783569335, 0.16285931396484374),
vm.Point3D(0.009508121490478515, -0.02874489402770996, 0.16285931396484374),
vm.Point3D(0.01073911190032959, -0.02879453659057617, 0.16285931396484374),
vm.Point3D(0.011898954391479493, -0.02870889663696289, 0.16285931396484374),
vm.Point3D(0.01304564380645752, -0.028496240615844725, 0.16285931396484374),
vm.Point3D(0.037929359436035155, -0.023318639755249025, 0.16285931396484374),
vm.Point3D(0.04026692581176758, -0.022659902572631837, 0.16285931396484374),
vm.Point3D(0.0423753433227539, -0.02173179054260254, 0.16285931396484374),
vm.Point3D(0.043635421752929685, -0.021140312194824217, 0.16285931396484374),
vm.Point3D(0.045726459503173826, -0.019112783432006834, 0.16285931396484374),
vm.Point3D(0.046045814514160156, -0.018350631713867187, 0.16285931396484374),
vm.Point3D(0.046317790985107424, -0.017561525344848634, 0.16285931396484374),
vm.Point3D(0.04654034042358399, -0.01675141906738281, 0.16285931396484374),
vm.Point3D(0.046711788177490235, -0.015926435470581056, 0.16285931396484374),
vm.Point3D(0.053979331970214844, 0.020638671875, 0.16285931396484374),
vm.Point3D(0.053991470336914066, 0.020810815811157228, 0.16285931396484374),
vm.Point3D(0.053973892211914065, 0.020982486724853516, 0.16285931396484374),
vm.Point3D(0.05395987319946289, 0.021073774337768556, 0.16285931396484374),
vm.Point3D(0.05268712615966797, 0.025928991317749023, 0.16285931396484374),
vm.Point3D(0.05260356140136719, 0.026217063903808593, 0.16285931396484374),
vm.Point3D(0.0053228259086608885, 0.1313191223144531, 0.16285931396484374),
vm.Point3D(0.00030017581582069395, 0.13677394104003907, 0.16285931396484374),
vm.Point3D(-0.0014313015937805177, 0.1385874481201172, 0.16285931396484374),
vm.Point3D(-0.003362513303756714, 0.14024832153320313, 0.16285931396484374),
vm.Point3D(-0.013057180404663086, 0.14319378662109375, 0.16285931396484374)],
    [vm.Point3D(-0.032552875518798825, 0.18903926086425782, 0.21148847113715277),
vm.Point3D(-0.03902994537353516, 0.18896835327148437, 0.21148847113715277),
vm.Point3D(-0.045451812744140625, 0.1882697296142578, 0.21148847113715277),
vm.Point3D(-0.05175935745239258, 0.1869498291015625, 0.21148847113715277),
vm.Point3D(-0.05789449310302734, 0.1850208282470703, 0.21148847113715277),
vm.Point3D(-0.06380073547363281, 0.18250044250488281, 0.21148847113715277),
vm.Point3D(-0.0719752426147461, 0.1776184539794922, 0.21148847113715277),
vm.Point3D(-0.07209098815917969, 0.1775470428466797, 0.21148847113715277),
vm.Point3D(-0.07238782501220703, 0.1773623504638672, 0.21148847113715277),
vm.Point3D(-0.07606041717529297, 0.1748844451904297, 0.21148847113715277),
vm.Point3D(-0.07725887298583985, 0.17399330139160157, 0.21148847113715277),
vm.Point3D(-0.07953073883056641, 0.17218084716796875, 0.21148847113715277),
vm.Point3D(-0.08017269134521485, 0.1716375732421875, 0.21148847113715277),
vm.Point3D(-0.08216158294677735, 0.16985983276367186, 0.21148847113715277),
vm.Point3D(-0.0828564682006836, 0.16920291137695312, 0.21148847113715277),
vm.Point3D(-0.08401498413085938, 0.16806324768066405, 0.21148847113715277),
vm.Point3D(-0.08599291229248048, 0.16597808837890626, 0.21148847113715277),
vm.Point3D(-0.08663853454589844, 0.1652559356689453, 0.21148847113715277),
vm.Point3D(-0.08756526947021484, 0.16418037414550782, 0.21148847113715277),
vm.Point3D(-0.0890186538696289, 0.16245500183105469, 0.21148847113715277),
vm.Point3D(-0.09172274780273437, 0.1587900390625, 0.21148847113715277),
vm.Point3D(-0.09418171691894531, 0.154925537109375, 0.21148847113715277),
vm.Point3D(-0.09641954040527344, 0.1508263854980469, 0.21148847113715277),
vm.Point3D(-0.09834632873535157, 0.14665037536621095, 0.21148847113715277),
vm.Point3D(-0.09998783874511719, 0.14234471130371093, 0.21148847113715277),
vm.Point3D(-0.1013353042602539, 0.1379343566894531, 0.21148847113715277),
vm.Point3D(-0.10238275909423829, 0.1334447784423828, 0.21148847113715277),
vm.Point3D(-0.10312690734863281, 0.1289015655517578, 0.21148847113715277),
vm.Point3D(-0.10356690216064453, 0.12442110443115234, 0.21148847113715277),
vm.Point3D(-0.10372638702392578, 0.11988057708740234, 0.21148847113715277),
vm.Point3D(-0.10359210968017578, 0.11535820007324218, 0.21148847113715277),
vm.Point3D(-0.10305767822265625, 0.11002735900878906, 0.21148847113715277),
vm.Point3D(-0.10212653350830078, 0.10477787017822265, 0.21148847113715277),
vm.Point3D(-0.10080961608886718, 0.09963277435302734, 0.21148847113715277),
vm.Point3D(-0.10000993347167969, 0.09710636138916015, 0.21148847113715277),
vm.Point3D(-0.09911802673339844, 0.09461454010009765, 0.21148847113715277),
vm.Point3D(-0.09813543701171876, 0.09216036987304688, 0.21148847113715277),
vm.Point3D(-0.03370913696289062, -0.058159008026123046, 0.21148847113715277),
vm.Point3D(-0.032856101989746096, -0.05874211883544922, 0.21148847113715277),
vm.Point3D(-0.0319820327758789, -0.05931711578369141, 0.21148847113715277),
vm.Point3D(-0.031112964630126954, -0.05986687088012695, 0.21148847113715277),
vm.Point3D(-0.0296524658203125, -0.0595878791809082, 0.21148847113715277),
vm.Point3D(-0.02444703483581543, -0.05800255584716797, 0.21148847113715277),
vm.Point3D(0.057712776184082035, -0.030171194076538087, 0.21148847113715277),
vm.Point3D(0.08078765106201172, -0.022217842102050783, 0.21148847113715277),
vm.Point3D(0.08118883514404297, -0.022066390991210938, 0.21148847113715277),
vm.Point3D(0.08125575256347656, -0.02203432846069336, 0.21148847113715277),
vm.Point3D(0.08161629486083985, -0.021821744918823244, 0.21148847113715277),
vm.Point3D(0.08168018341064454, -0.02177606773376465, 0.21148847113715277),
vm.Point3D(0.08199049377441406, -0.021510107040405273, 0.21148847113715277),
vm.Point3D(0.08204832458496093, -0.021450748443603517, 0.21148847113715277),
vm.Point3D(0.0823005142211914, -0.021140567779541014, 0.21148847113715277),
vm.Point3D(0.08234918975830079, -0.02106806182861328, 0.21148847113715277),
vm.Point3D(0.08253732299804688, -0.020723901748657226, 0.21148847113715277),
vm.Point3D(0.08255496215820313, -0.020684097290039064, 0.21148847113715277),
vm.Point3D(0.08257383728027344, -0.020639404296875, 0.21148847113715277),
vm.Point3D(0.08259023284912109, -0.020598588943481447, 0.21148847113715277),
vm.Point3D(0.08260577392578125, -0.020557939529418947, 0.21148847113715277),
vm.Point3D(0.08273110198974609, -0.020096532821655272, 0.21148847113715277),
vm.Point3D(0.09306076049804687, 0.023186473846435546, 0.21148847113715277),
vm.Point3D(0.09339018249511719, 0.07300833129882812, 0.21148847113715277),
vm.Point3D(0.018647174835205078, 0.1631864013671875, 0.21148847113715277),
vm.Point3D(0.014239314079284669, 0.16812294006347656, 0.21148847113715277),
vm.Point3D(0.009396167755126953, 0.17262370300292967, 0.21148847113715277),
vm.Point3D(0.004162330150604248, 0.17664724731445314, 0.21148847113715277),
vm.Point3D(-0.0014140068292617799, 0.18015653991699218, 0.21148847113715277),
vm.Point3D(-0.007281498908996582, 0.1831192626953125, 0.21148847113715277),
vm.Point3D(-0.013386120796203613, 0.1855081329345703, 0.21148847113715277),
vm.Point3D(-0.019671663284301758, 0.1873011474609375, 0.21148847113715277),
vm.Point3D(-0.026080251693725586, 0.18848182678222655, 0.21148847113715277)],

    [vm.Point3D(-0.008207533836364746, 0.2508453674316406, 0.2601176283094618),
vm.Point3D(-0.084091064453125, 0.16704635620117186, 0.2601176283094618),
vm.Point3D(-0.08809623718261719, 0.16201771545410157, 0.2601176283094618),
vm.Point3D(-0.09159443664550782, 0.15660951232910156, 0.2601176283094618),
vm.Point3D(-0.09953105926513672, 0.1430395965576172, 0.2601176283094618),
vm.Point3D(-0.09999156951904296, 0.14165376281738282, 0.2601176283094618),
vm.Point3D(-0.10108388519287109, 0.13786744689941408, 0.2601176283094618),
vm.Point3D(-0.1022943344116211, 0.13339891052246095, 0.2601176283094618),
vm.Point3D(-0.10301695251464844, 0.12882789611816406, 0.2601176283094618),
vm.Point3D(-0.1034316177368164, 0.12422869873046875, 0.2601176283094618),
vm.Point3D(-0.10370508575439454, 0.11975404357910156, 0.2601176283094618),
vm.Point3D(-0.10354524993896484, 0.11519697570800781, 0.2601176283094618),
vm.Point3D(-0.10297544097900391, 0.10982662963867187, 0.2601176283094618),
vm.Point3D(-0.1025392303466797, 0.10717151641845703, 0.2601176283094618),
vm.Point3D(-0.10200409698486328, 0.10454054260253906, 0.2601176283094618),
vm.Point3D(-0.10137150573730469, 0.1019366455078125, 0.2601176283094618),
vm.Point3D(-0.10064292907714843, 0.09936270904541016, 0.2601176283094618),
vm.Point3D(-0.0998199005126953, 0.0968216323852539, 0.2601176283094618),
vm.Point3D(-0.09890399932861328, 0.09431640625, 0.2601176283094618),
vm.Point3D(-0.03711124801635742, -0.059255661010742186, 0.2601176283094618),
vm.Point3D(-0.03666657257080078, -0.06018813705444336, 0.2601176283094618),
vm.Point3D(-0.03661773681640625, -0.06027912902832031, 0.2601176283094618),
vm.Point3D(-0.03604153823852539, -0.06109286117553711, 0.2601176283094618),
vm.Point3D(-0.031743526458740234, -0.06654579162597657, 0.2601176283094618),
vm.Point3D(-0.03086210060119629, -0.06740702056884766, 0.2601176283094618),
vm.Point3D(-0.029855182647705078, -0.06803736877441406, 0.2601176283094618),
vm.Point3D(-0.02984282684326172, -0.06804441070556641, 0.2601176283094618),
vm.Point3D(-0.029214427947998046, -0.06835525512695312, 0.2601176283094618),
vm.Point3D(-0.02915687370300293, -0.0683835678100586, 0.2601176283094618),
vm.Point3D(-0.02816290283203125, -0.06875208282470703, 0.2601176283094618),
vm.Point3D(-0.01601919746398926, -0.07303746795654296, 0.2601176283094618),
vm.Point3D(-0.015049818992614747, -0.07336737823486328, 0.2601176283094618),
vm.Point3D(-0.014826391220092773, -0.07343647003173828, 0.2601176283094618),
vm.Point3D(-0.013791533470153808, -0.0735477294921875, 0.2601176283094618),
vm.Point3D(-0.013688020706176758, -0.07355876922607422, 0.2601176283094618),
vm.Point3D(-0.011684782028198242, -0.07364190673828125, 0.2601176283094618),
vm.Point3D(-0.01074007511138916, -0.07354588317871094, 0.2601176283094618),
vm.Point3D(-0.010693093299865723, -0.07354100799560546, 0.2601176283094618),
vm.Point3D(-0.009747095108032226, -0.07325525665283203, 0.2601176283094618),
vm.Point3D(0.07549286651611328, -0.03827386093139649, 0.2601176283094618),
vm.Point3D(0.07594464111328125, -0.03804726409912109, 0.2601176283094618),
vm.Point3D(0.0763506851196289, -0.03774609756469727, 0.2601176283094618),
vm.Point3D(0.07669914245605469, -0.037379138946533205, 0.2601176283094618),
vm.Point3D(0.07695381164550781, -0.037093746185302735, 0.2601176283094618),
vm.Point3D(0.07722650909423828, -0.036680694580078124, 0.2601176283094618),
vm.Point3D(0.07736872100830078, -0.03637439727783203, 0.2601176283094618),
vm.Point3D(0.0775263900756836, -0.03600359344482422, 0.2601176283094618),
vm.Point3D(0.07754278564453125, -0.035962779998779296, 0.2601176283094618),
vm.Point3D(0.07755848693847656, -0.03592169570922851, 0.2601176283094618),
vm.Point3D(0.0776082763671875, -0.03577490234375, 0.2601176283094618),
vm.Point3D(0.0971041488647461, 0.029485403060913087, 0.2601176283094618),
vm.Point3D(0.09790062713623048, 0.0323336067199707, 0.2601176283094618),
vm.Point3D(0.09856843566894531, 0.03556864929199219, 0.2601176283094618),
vm.Point3D(0.09909113311767578, 0.03911087799072266, 0.2601176283094618),
vm.Point3D(0.09945584869384766, 0.042873065948486326, 0.2601176283094618),
vm.Point3D(0.09965361022949219, 0.046762580871582034, 0.2601176283094618),
vm.Point3D(0.09967953491210937, 0.050683643341064455, 0.2601176283094618),
vm.Point3D(0.09953298950195312, 0.054539710998535156, 0.2601176283094618),
vm.Point3D(0.09921759033203124, 0.05823583221435547, 0.2601176283094618),
vm.Point3D(0.0987410888671875, 0.06168099594116211, 0.2601176283094618),
vm.Point3D(0.09811522674560547, 0.06479036712646484, 0.2601176283094618),
vm.Point3D(0.06331784057617187, 0.21443923950195312, 0.2601176283094618),
vm.Point3D(0.06290574645996094, 0.21608450317382813, 0.2601176283094618),
vm.Point3D(0.06269189071655273, 0.21675541687011718, 0.2601176283094618),
vm.Point3D(0.06253605270385743, 0.21719694519042967, 0.2601176283094618),
vm.Point3D(0.06234354019165039, 0.21770094299316406, 0.2601176283094618),
vm.Point3D(0.06169289779663086, 0.21916445922851563, 0.2601176283094618),
vm.Point3D(0.0613367919921875, 0.21985302734375, 0.2601176283094618),
vm.Point3D(0.06043319320678711, 0.22135943603515626, 0.2601176283094618),
vm.Point3D(0.05949412536621094, 0.22266343688964843, 0.2601176283094618),
vm.Point3D(0.05846425247192383, 0.22387586975097656, 0.2601176283094618),
vm.Point3D(0.05762709426879883, 0.22473118591308594, 0.2601176283094618),
vm.Point3D(0.057347785949707034, 0.22499436950683593, 0.2601176283094618),
vm.Point3D(0.056083263397216795, 0.22606521606445312, 0.2601176283094618),
vm.Point3D(0.05604710006713867, 0.22609315490722656, 0.2601176283094618),
vm.Point3D(0.054638179779052734, 0.22708189392089845, 0.2601176283094618),
vm.Point3D(0.05370331573486328, 0.22763909912109376, 0.2601176283094618),
vm.Point3D(0.03403970718383789, 0.2388927764892578, 0.2601176283094618),
vm.Point3D(0.0011959041357040405, 0.25031782531738284, 0.2601176283094618),
vm.Point3D(0.0011366173028945924, 0.25033729553222656, 0.2601176283094618),
vm.Point3D(0.0006921873092651368, 0.25044749450683595, 0.2601176283094618),
vm.Point3D(0.00024115948379039765, 0.25049554443359373, 0.2601176283094618)],
    [vm.Point3D(-0.010604868888854981, 0.25544769287109376, 0.3087467854817708),
vm.Point3D(-0.03124400520324707, -0.05455257415771484, 0.3087467854817708),
vm.Point3D(-0.03130274772644043, -0.05558409118652344, 0.3087467854817708),
vm.Point3D(-0.031189207077026368, -0.056608932495117184, 0.3087467854817708),
vm.Point3D(-0.0309064884185791, -0.05760097122192383, 0.3087467854817708),
vm.Point3D(-0.03046185874938965, -0.05853323364257813, 0.3087467854817708),
vm.Point3D(-0.03041231346130371, -0.05862467575073242, 0.3087467854817708),
vm.Point3D(-0.027614965438842773, -0.06287195587158204, 0.3087467854817708),
vm.Point3D(-0.026767383575439452, -0.06399352264404297, 0.3087467854817708),
vm.Point3D(-0.025745052337646485, -0.06492023468017578, 0.3087467854817708),
vm.Point3D(-0.02460012626647949, -0.06561465454101563, 0.3087467854817708),
vm.Point3D(-0.02459031105041504, -0.06561975860595703, 0.3087467854817708),
vm.Point3D(-0.02404205131530762, -0.06585366821289063, 0.3087467854817708),
vm.Point3D(-0.02292808723449707, -0.06627790069580078, 0.3087467854817708),
vm.Point3D(-0.02278839874267578, -0.06631626892089844, 0.3087467854817708),
vm.Point3D(-0.012440189361572266, -0.06895392608642578, 0.3087467854817708),
vm.Point3D(-0.012259869575500489, -0.06899011993408204, 0.3087467854817708),
vm.Point3D(-0.011183531761169433, -0.06917070007324219, 0.3087467854817708),
vm.Point3D(-0.010918049812316895, -0.06917656707763672, 0.3087467854817708),
vm.Point3D(-0.010076598167419433, -0.06914939880371093, 0.3087467854817708),
vm.Point3D(-0.009998991966247558, -0.06914490509033203, 0.3087467854817708),
vm.Point3D(-0.009753141403198242, -0.06911286926269532, 0.3087467854817708),
vm.Point3D(-0.00829634952545166, -0.06890043640136718, 0.3087467854817708),
vm.Point3D(-0.0072723708152770995, -0.06864768218994141, 0.3087467854817708),
vm.Point3D(0.038089847564697264, -0.05439760971069336, 0.3087467854817708),
vm.Point3D(0.039809425354003905, -0.053730983734130856, 0.3087467854817708),
vm.Point3D(0.03985519027709961, -0.05371197891235351, 0.3087467854817708),
vm.Point3D(0.0407705078125, -0.05333186721801758, 0.3087467854817708),
vm.Point3D(0.04092917251586914, -0.05326324462890625, 0.3087467854817708),
vm.Point3D(0.04226494598388672, -0.0526662483215332, 0.3087467854817708),
vm.Point3D(0.042336688995361325, -0.05262675476074219, 0.3087467854817708),
vm.Point3D(0.04363461685180664, -0.05177023696899414, 0.3087467854817708),
vm.Point3D(0.07080381774902343, -0.032085441589355466, 0.3087467854817708),
vm.Point3D(0.07109381103515625, -0.03184650230407715, 0.3087467854817708),
vm.Point3D(0.07119570922851562, -0.03174713706970215, 0.3087467854817708),
vm.Point3D(0.07142466735839843, -0.03148546600341797, 0.3087467854817708),
vm.Point3D(0.07152546691894532, -0.03134865951538086, 0.3087467854817708),
vm.Point3D(0.07169377136230469, -0.0310775203704834, 0.3087467854817708),
vm.Point3D(0.07544326782226562, -0.023758499145507813, 0.3087467854817708),
vm.Point3D(0.07592865753173828, -0.022711578369140624, 0.3087467854817708),
vm.Point3D(0.07603355407714844, -0.02242930030822754, 0.3087467854817708),
vm.Point3D(0.07628166961669922, -0.02160985565185547, 0.3087467854817708),
vm.Point3D(0.08193292236328124, 0.0007950757145881652, 0.3087467854817708),
vm.Point3D(0.08195355987548827, 0.0008994390368461609, 0.3087467854817708),
vm.Point3D(0.08201879119873047, 0.0014486271142959595, 0.3087467854817708),
vm.Point3D(0.0847984390258789, 0.025660154342651367, 0.3087467854817708),
vm.Point3D(0.08456723022460938, 0.02781087112426758, 0.3087467854817708),
vm.Point3D(0.06200638580322266, 0.1962295379638672, 0.3087467854817708),
vm.Point3D(0.04999650192260742, 0.22541395568847655, 0.3087467854817708),
vm.Point3D(0.04957948303222656, 0.2264048614501953, 0.3087467854817708),
vm.Point3D(0.04919685363769531, 0.2271392822265625, 0.3087467854817708),
vm.Point3D(0.04901335144042969, 0.2274542236328125, 0.3087467854817708),
vm.Point3D(0.04851024627685547, 0.22820054626464845, 0.3087467854817708),
vm.Point3D(0.048066974639892575, 0.22883103942871094, 0.3087467854817708),
vm.Point3D(0.047599201202392576, 0.2294507598876953, 0.3087467854817708),
vm.Point3D(0.04647229385375977, 0.23070252990722656, 0.3087467854817708),
vm.Point3D(0.04495684432983398, 0.23210064697265625, 0.3087467854817708),
vm.Point3D(0.043595314025878906, 0.23318142700195313, 0.3087467854817708),
vm.Point3D(0.02427046012878418, 0.24751808166503905, 0.3087467854817708),
vm.Point3D(0.023547840118408204, 0.2479903106689453, 0.3087467854817708),
vm.Point3D(0.022732593536376952, 0.24846820068359374, 0.3087467854817708),
vm.Point3D(0.02045680236816406, 0.24974369812011718, 0.3087467854817708),
vm.Point3D(0.018347965240478516, 0.2508174591064453, 0.3087467854817708),
vm.Point3D(0.016428760528564453, 0.2516969757080078, 0.3087467854817708),
vm.Point3D(0.014683937072753906, 0.25240689086914064, 0.3087467854817708),
vm.Point3D(0.013209285736083985, 0.25295291137695314, 0.3087467854817708),
vm.Point3D(0.011449973106384277, 0.25353517150878907, 0.3087467854817708),
vm.Point3D(0.00789752197265625, 0.25469747924804687, 0.3087467854817708),
vm.Point3D(0.006583809375762939, 0.2550425567626953, 0.3087467854817708),
vm.Point3D(0.0052326183319091795, 0.2552791137695313, 0.3087467854817708),
vm.Point3D(0.002556457042694092, 0.2554306640625, 0.3087467854817708),
vm.Point3D(-7.359097152948379e-05, 0.25544367980957033, 0.3087467854817708)],
  [vm.Point3D(-0.010337559700012208, 0.2539773406982422, 0.35737594265407985),
vm.Point3D(-0.06056604766845703, 0.1809791259765625, 0.35737594265407985),
vm.Point3D(-0.06264878845214844, 0.17779869079589844, 0.35737594265407985),
vm.Point3D(-0.06454641723632812, 0.17449867248535156, 0.35737594265407985),
vm.Point3D(-0.06625284576416016, 0.1710896759033203, 0.35737594265407985),
vm.Point3D(-0.06776260375976563, 0.1675826416015625, 0.35737594265407985),
vm.Point3D(-0.03099472999572754, -0.016465999603271483, 0.35737594265407985),
vm.Point3D(0.00011939946562051773, -0.028929946899414062, 0.35737594265407985),
vm.Point3D(0.008953878402709961, -0.031650068283081055, 0.35737594265407985),
vm.Point3D(0.01601616096496582, -0.032472736358642576, 0.35737594265407985),
vm.Point3D(0.016151466369628907, -0.032484115600585936, 0.35737594265407985),
vm.Point3D(0.01800291633605957, -0.032633598327636716, 0.35737594265407985),
vm.Point3D(0.02400084686279297, -0.03239154052734375, 0.35737594265407985),
vm.Point3D(0.024132179260253905, -0.0323820915222168, 0.35737594265407985),
vm.Point3D(0.028423372268676757, -0.03200579071044922, 0.35737594265407985),
vm.Point3D(0.028536632537841798, -0.031995704650878906, 0.35737594265407985),
vm.Point3D(0.03223592758178711, -0.031598533630371094, 0.35737594265407985),
vm.Point3D(0.032329875946044924, -0.03158794021606445, 0.35737594265407985),
vm.Point3D(0.034135391235351566, -0.031380403518676755, 0.35737594265407985),
vm.Point3D(0.03728248596191406, -0.03095427703857422, 0.35737594265407985),
vm.Point3D(0.03735775375366211, -0.03094300651550293, 0.35737594265407985),
vm.Point3D(0.03915735626220703, -0.030536428451538086, 0.35737594265407985),
vm.Point3D(0.06156253433227539, -0.023823749542236327, 0.35737594265407985),
vm.Point3D(0.06355305862426758, -0.020320634841918945, 0.35737594265407985),
vm.Point3D(0.06498668670654296, -0.01654608726501465, 0.35737594265407985),
vm.Point3D(0.07735415649414062, 0.02623099136352539, 0.35737594265407985),
vm.Point3D(0.0775024642944336, 0.02699221420288086, 0.35737594265407985),
vm.Point3D(0.07751750183105469, 0.027767602920532226, 0.35737594265407985),
vm.Point3D(0.06415316772460937, 0.14600100708007813, 0.35737594265407985),
vm.Point3D(0.06364022827148437, 0.1503155975341797, 0.35737594265407985),
vm.Point3D(0.06283378601074219, 0.15463925170898438, 0.35737594265407985),
vm.Point3D(0.04887517929077148, 0.21696682739257814, 0.35737594265407985),
vm.Point3D(0.0481314697265625, 0.2197353515625, 0.35737594265407985),
vm.Point3D(0.04688597869873047, 0.22230909729003906, 0.35737594265407985),
vm.Point3D(0.04601916885375976, 0.22409060668945313, 0.35737594265407985),
vm.Point3D(0.04540784454345703, 0.22516009521484376, 0.35737594265407985),
vm.Point3D(0.04490259552001953, 0.22586524963378907, 0.35737594265407985),
vm.Point3D(0.04400514984130859, 0.22701016235351562, 0.35737594265407985),
vm.Point3D(0.04322865676879883, 0.227889892578125, 0.35737594265407985),
vm.Point3D(0.04302326965332031, 0.22811015319824218, 0.35737594265407985),
vm.Point3D(0.04264113235473633, 0.22851724243164062, 0.35737594265407985),
vm.Point3D(0.03153894805908203, 0.2401744384765625, 0.35737594265407985),
vm.Point3D(0.03085706901550293, 0.24083074951171876, 0.35737594265407985),
vm.Point3D(0.030291120529174806, 0.2413599853515625, 0.35737594265407985),
vm.Point3D(0.029771217346191405, 0.24174554443359375, 0.35737594265407985),
vm.Point3D(0.0289350643157959, 0.24235107421875, 0.35737594265407985),
vm.Point3D(0.017219924926757814, 0.2500207977294922, 0.35737594265407985),
vm.Point3D(0.013010541915893554, 0.25225938415527344, 0.35737594265407985),
vm.Point3D(0.011754136085510253, 0.25260917663574217, 0.35737594265407985),
vm.Point3D(0.010459518432617188, 0.2528188171386719, 0.35737594265407985),
vm.Point3D(0.006894575595855713, 0.2533437805175781, 0.35737594265407985)],
 
  [vm.Point3D(-0.013217350006103516, 0.23776652526855468, 0.4060050998263889),
vm.Point3D(-0.10356132507324219, 0.203, 0.4060050998263889),
vm.Point3D(-0.10356132507324219, 0.103, 0.4060050998263889),
vm.Point3D(-0.08557473754882812, -0.030014928817749024, 0.4060050998263889),
vm.Point3D(-0.0852157211303711, -0.0323322982788086, 0.4060050998263889),
vm.Point3D(-0.08362799835205079, -0.04227001953125, 0.4060050998263889),
vm.Point3D(-0.08318868255615235, -0.044697498321533205, 0.4060050998263889),
vm.Point3D(-0.08317271423339843, -0.04477408218383789, 0.4060050998263889),
vm.Point3D(-0.08201930999755859, -0.04983098220825195, 0.4060050998263889),
vm.Point3D(-0.08182829284667968, -0.05040631866455078, 0.4060050998263889),
vm.Point3D(-0.08162610626220704, -0.05073894500732422, 0.4060050998263889),
vm.Point3D(-0.08133731079101562, -0.051135498046875, 0.4060050998263889),
vm.Point3D(-0.08112034606933594, -0.051219390869140624, 0.4060050998263889),
vm.Point3D(-0.07369345092773437, -0.05123001480102539, 0.4060050998263889),
vm.Point3D(0.028710474014282228, -0.03126677894592285, 0.4060050998263889),
vm.Point3D(0.030405200958251954, -0.030437047958374024, 0.4060050998263889),
vm.Point3D(0.04058710479736328, -0.023716938018798827, 0.4060050998263889),
vm.Point3D(0.04204640197753906, -0.022171638488769532, 0.4060050998263889),
vm.Point3D(0.043107898712158206, -0.020408784866333008, 0.4060050998263889),
vm.Point3D(0.04392776870727539, -0.018527910232543944, 0.4060050998263889),
vm.Point3D(0.04445206069946289, -0.016605672836303712, 0.4060050998263889),
vm.Point3D(0.044755512237548825, -0.014668251037597656, 0.4060050998263889),
vm.Point3D(0.044921459197998045, -0.012702741622924806, 0.4060050998263889),
vm.Point3D(0.04754342269897461, 0.10069173431396485, 0.4060050998263889),
vm.Point3D(0.040554115295410156, 0.20180389404296875, 0.4060050998263889),
vm.Point3D(0.04034128189086914, 0.20320819091796874, 0.4060050998263889),
vm.Point3D(0.040192230224609375, 0.20388650512695314, 0.4060050998263889),
vm.Point3D(0.039566326141357425, 0.20588699340820313, 0.4060050998263889),
vm.Point3D(0.03494860458374023, 0.21929313659667968, 0.4060050998263889),
vm.Point3D(0.03460895919799805, 0.22026101684570312, 0.4060050998263889),
vm.Point3D(0.03441640090942383, 0.22077450561523437, 0.4060050998263889),
vm.Point3D(0.034212154388427736, 0.22129994201660155, 0.4060050998263889),
vm.Point3D(0.03330986404418945, 0.2234527587890625, 0.4060050998263889),
vm.Point3D(0.02900913429260254, 0.2334222106933594, 0.4060050998263889),
vm.Point3D(0.028679754257202147, 0.2338262939453125, 0.4060050998263889),
vm.Point3D(0.02543634033203125, 0.2358076171875, 0.4060050998263889),
vm.Point3D(0.024662160873413087, 0.23622085571289062, 0.4060050998263889),
vm.Point3D(0.023807098388671875, 0.23659071350097657, 0.4060050998263889),
vm.Point3D(0.023108455657958986, 0.23683187866210936, 0.4060050998263889),
vm.Point3D(0.022096643447875975, 0.2370916748046875, 0.4060050998263889),
vm.Point3D(0.02151949119567871, 0.23719499206542968, 0.4060050998263889),
vm.Point3D(0.02037856864929199, 0.2373074188232422, 0.4060050998263889),
vm.Point3D(0.02002399444580078, 0.2373179931640625, 0.4060050998263889)],
   
  [vm.Point3D(-0.011512272834777832, 0.23403472900390626, 0.45463425699869786),
vm.Point3D(-0.03077821922302246, 0.2310986633300781, 0.45463425699869786),
vm.Point3D(-0.08233112335205078, 0.203, 0.45463425699869786),
vm.Point3D(-0.08725215911865235, 0.19043856811523438, 0.45463425699869786),
vm.Point3D(-0.09251079559326172, 0.15651051330566407, 0.45463425699869786),
vm.Point3D(-0.09253170013427735, 0.15633479309082032, 0.45463425699869786),
vm.Point3D(-0.09255121612548828, 0.1560577392578125, 0.45463425699869786),
vm.Point3D(-0.09256875610351563, 0.1556877899169922, 0.45463425699869786),
vm.Point3D(-0.09258379364013672, 0.1552361755371094, 0.45463425699869786),
vm.Point3D(-0.09259586334228516, 0.15471661376953125, 0.45463425699869786),
vm.Point3D(-0.09260459899902344, 0.15414488220214845, 0.45463425699869786),
vm.Point3D(-0.0926097412109375, 0.15353837585449218, 0.45463425699869786),
vm.Point3D(-0.09261112213134766, 0.15291551208496093, 0.45463425699869786),
vm.Point3D(-0.09260871124267578, 0.15229521179199218, 0.45463425699869786),
vm.Point3D(-0.09260258483886719, 0.15169631958007812, 0.45463425699869786),
vm.Point3D(-0.09259291076660156, 0.15113705444335937, 0.45463425699869786),
vm.Point3D(-0.09258000183105469, 0.15063438415527344, 0.45463425699869786),
vm.Point3D(-0.09256423950195312, 0.15020358276367188, 0.45463425699869786),
vm.Point3D(-0.09254610443115234, 0.14985777282714843, 0.45463425699869786),
vm.Point3D(-0.08024741363525391, -0.04357291030883789, 0.45463425699869786),
vm.Point3D(-0.07995290374755859, -0.04515132141113281, 0.45463425699869786),
vm.Point3D(0.034438331604003905, 0.17120187377929688, 0.45463425699869786),
vm.Point3D(0.03811129379272461, 0.19251608276367188, 0.45463425699869786),
vm.Point3D(0.03812942123413086, 0.19339324951171874, 0.45463425699869786),
vm.Point3D(0.03808805084228516, 0.19384791564941406, 0.45463425699869786),
vm.Point3D(0.03522410202026367, 0.21109030151367186, 0.45463425699869786),
vm.Point3D(0.034992782592773435, 0.21206349182128906, 0.45463425699869786),
vm.Point3D(0.03475240707397461, 0.21288121032714843, 0.45463425699869786),
vm.Point3D(0.03409056854248047, 0.21462547302246093, 0.45463425699869786),
vm.Point3D(0.032803272247314455, 0.21703118896484375, 0.45463425699869786),
vm.Point3D(0.031159225463867186, 0.2192277069091797, 0.45463425699869786),
vm.Point3D(0.029825468063354493, 0.22060514831542968, 0.45463425699869786),
vm.Point3D(0.016556486129760743, 0.22996449279785156, 0.45463425699869786),
vm.Point3D(0.01528004264831543, 0.23079084777832032, 0.45463425699869786),
vm.Point3D(0.013834228515625, 0.23153396606445312, 0.45463425699869786),
vm.Point3D(0.01293502140045166, 0.23190548706054687, 0.45463425699869786),
vm.Point3D(0.012372482299804687, 0.23210536193847656, 0.45463425699869786),
vm.Point3D(0.010871953010559082, 0.23252365112304688, 0.45463425699869786),
vm.Point3D(0.010421835899353027, 0.23261795043945313, 0.45463425699869786),
vm.Point3D(0.009354467391967774, 0.23278622436523438, 0.45463425699869786),
vm.Point3D(0.004968397617340088, 0.23321089172363282, 0.45463425699869786),
vm.Point3D(0.0036235508918762206, 0.23333177185058593, 0.45463425699869786),
vm.Point3D(0.002219841480255127, 0.23344364929199218, 0.45463425699869786),
vm.Point3D(0.001825914740562439, 0.23347267150878906, 0.45463425699869786),
vm.Point3D(0.00043767109513282777, 0.23356747436523437, 0.45463425699869786),
vm.Point3D(6.725972890853882e-05, 0.23359091186523437, 0.45463425699869786),
vm.Point3D(-0.0010554556846618652, 0.2336575469970703, 0.45463425699869786),
vm.Point3D(-0.0025991556644439696, 0.23373916625976562, 0.45463425699869786),
vm.Point3D(-0.004197282314300537, 0.2338126678466797, 0.45463425699869786),
vm.Point3D(-0.004853758335113525, 0.23383990478515626, 0.45463425699869786),
vm.Point3D(-0.005854502201080323, 0.23387832641601564, 0.45463425699869786),
vm.Point3D(-0.007570804119110108, 0.23393612670898437, 0.45463425699869786),
vm.Point3D(-0.00794718599319458, 0.233947509765625, 0.45463425699869786),
vm.Point3D(-0.00964542293548584, 0.23399354553222657, 0.45463425699869786)]
]

polygons = []
for polygon_points in polygons_points:
    polygons.append(vmw.ClosedPolygon3D(polygon_points))



dict_closing = []
list_closing_point = []
count = 0
for i, i_polygon in enumerate(polygons):
    i_polygon = i_polygon.simplify()
    for j, j_polygon in enumerate(polygons):
        if i > j:
            faces=[]
            j_polygon = j_polygon.simplify()
            coords = i_polygon.sewing(j_polygon, vm.X3D, vm.Y3D)
            for trio in coords :
                faces.append(vmf.Triangle3D(trio[0], trio[1], trio[2]))
            
            volum = volmdlr.core.VolumeModel(faces)
            # volum.babylonjs()
        break
    if i > 0:
        break
            
