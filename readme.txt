Spells are taken from the WotC Sourcebook Spell Compendium which itself is a collection of spells that WotC previously published in other sources, e.g. the Complete Adventurer Sourcebook.
Temple+ is needed!

Custom .mes filenames are all named spell_compendium_x.mes, partsys is spell_compendium_partsys.tab and protos.tab is spell_compendium_protos.tab
Uses customized history.mes and damage.mes, which are included so be careful. Both are not customizable.

finished = finished with maybe exceptions of cosmetics; WAT = Wrong Action (should be swift); functional = works but has minor functional errors; WIP = Work in Progress

ID      Spell Name                  SC Page Status      Comments
1050    Sound Lance                 196     functional  but spell ignores Silence spell I belive
1051    Critical Strike              56     WAT         
1052    Camouflage                   43     finished    rfu
1053    Appraising Touch             15     finished    rfu
1054    Phantom Threat              157     finished    check for ranged missing wonky; check for cannot be flanked missing (unsure if needed)
1055    Distort Speech               69     WIP         fixed freeform error, needs new test; needs only Verbal spells activation
1056    Distract                     69     finished    rfu
1057    Focusing Chant               96     WAT         should be swift
1058    Herald's Call               113     finished    rfu
1059    Improvisation               121     WIP         fully working, just needs radial change to dynamic; no sound.
1060    Joyful Noise                                    not yet started
1061    Inspirational Boost                             needs a c++ modification.
1062    Invisibility, Swift         125     WAT         should be swift, uses invisibilty condition; fully working
1063    Ironguts                    126     finished    uses nauseated as a secondary condition; rfu
1064    Ironthunder Horn            126     finished    rfu
1065    Insidious Rhythm                    finished    rfu
1066    Master's Touch              139     WAT         should be swift, untested: masterwork shield, magic shield; needs archery test
1067    Serene Visage               182     finished    rfu
1068    Shock and Awe               189     finished    
1069    Sticky Fingers              206     finished    need rework of particles; sound and buff symbol
1070    Undersong                   227     finished
1071    Distract Assailant           69     finished
1072    Insightfull Feint           124     functional  needs sound and different buff symbol; Unsure how to limit to feints, limited to combat atm
1073    Lightfoot                   132     WAT         should be swift
1074    Sniper's Shot               194     WIP         needs to be redone, semi functional for now
1075    Sonic Weapon                195     finished
1076    Bonefiddle                   37     finished
1077    Cloud of Bewilderment        48     finished    uses nauseated condition
1078    Curse of Impending Blades    56     finished
1079    Wave of Grief               236     finished
1080    Harmonic Chorus             110     finished    needs new buff symbol + sound; dismiss missing
1081    Iron Silence                125     finished
1082    War Cry                     236     WAT         should be swift; uses panicked condition
1084    Bladeweave                   31     finished    Uses dazed condition
1085    Fell the Greatest Foe        90     finished
1086    Fire Shuriken                92     finished    Uses Protos ID 4998 (spell_compendium_protos.tab) 
1087    Phantom Foe                 156     functional  Threat check is not perfect
1088    Veil of Shadow              228     finished
1089    Curse of Imp. Blades, Mass   57     finished
1090    Dissonant Chord              69     finished
1091    Haunting Tune               110     finished
1092    Love's Lament               134     finished
1093    Ray of Dizziness            166     finished
1094    Wounding Whispers           242     finished
1095    Dirge of Discord             66     finished
1096    Allegro                       9     finished    Check if only on friendly targets
1097    Find the Gap                 91     functional
1098    Wraithstrike                243     functional
1099    Resonating Bolt             174     finished
1100    Resistance, Greater         174     finished
1101    Fugue                       100     functional  DC40+ (attack an ally) disabled as it is not working
1102    Sirine's Grace              191     finished
1103    Dolorous Blow                70     finished
1104    Bolts of Bedevilment         37     WIP
1105    Cacophonic Burst             41     finished
1106    Wail of Doom                233     finished
1107    Heart Ripper                111     finished
1108    Dirge                        65     finished
1109    Nixie's Grace               148     finished
1110    Ray of Light                167     finished
1111    Resistance, Superior        174     finished
1112    Strategic Charge            210     WAT
1113    Blessed Aim                  31     finished
1114    Clear Mind                   47     finished
1115    Deafening Clang              59     WAT; WIP    does not deafen
1116    Grave Strike                107     needs cpp
1118    Faith Healing                87     finished
1119    Summon Undead I             215     finished
1120    Angelskin                    11     finished
1121    Demonhide                    63     finished
1122    Summon Undead II            215     finished
1123    Hand of Divinity            109     finished    uses modified deity.mes
1124    Curse of Ill Fortune         56     finished
1125    Awaken Sin                   21     finished
1126    Checkmates Light             46     finished
1127    Cloak of Bravery             47     finished
1128    Divine Protection            70     finished
1129    Quick March                 164     WAT
1130    Shield of Warding           188     finished
1131    Blessing of Bahamut          31     finished
1132    Diamondsteel                        not working
1133    Righteous Fury              177     finished
1134    Undead Bane Weapon          226     functional  is stacking with Weapon Bane; needs chain rework
1135    Weapon of the Deity         237     WIP
1136    Axiomatic Storm              22     finished
1137    Holy Storm                  115     finished
1138    Unholy Storm                227     finished
1139    Summon Undead III           215     finished
1140    Visage of the Deity, lesser 231     finished
1141    Lawful Sword                131     finished    needs chain rework
1142    Summon Undead IV            215     finished
1143    Castigate                    44     finished
1144    Summon Undead V             215     finished
1145    Conviction                   52     finished    check if buff symbol works
1146    Foundation of Stone          98     WIP         Needs check if own round
1147    Nightshield                 148     finished
1148    Nimbus of Light             148     finished
1149    Brambles                     38     finished
1150    Deific Vengeance             62     finished
1151    Frost Breath                100     finished
1152    Ghost Touch Armor           102     not working Uses 161 as Buff bonus type atm!
1153    Aid Mass                      8     finished    can't use original aid effect, due to changed max temp hp
1154    Align Weapon Mass             9     finished    Uses spell_radial_menu_options.mes
1155    Bless Weapon Swift           31     WAT
1156    Anarchic Storm               11     finished
1157    Clutch of Orcus              49     finished
1158    Conviction Mass              52     finished
1159    Corona of Cold               52     finished
1160    used for align weapon (which is not part of the spell_compendium)
1161    Demon Dirge                  63     finished
1162    Devil Blight                 64     finished
1163    Energy Vortex                81     finished    uses spell_radial_menu_options
1164    Grace                        
1165    Resist Energy Mass          174     finished    uses resist elements condition



Bonus Types: 151 Alchemical; 153 Sacred; 154 Profane; 160 Storm effects; 161 Ghost Touch Armor Property (needs to be verified that this is not in the game already!)

Latest Changes:
Added a python script(wf_ray_fix.py) that fixes WF(Ray) and switched all my ray spells to use it. Spells that do no call that script are NOT affected by this fix.

The two major advantages of this fix are you can a) now see it in the to hit history and b) it does not temporarily modify any attributes but behaves like the feat should behave in the first place.
This fix only works with temple+ !!

If you want to use the fix for your spells please feel free to do so.

Simply add in your ray spell in the "def OnBeginSpellCast(spell):" section the lines:
############   Weapon Focus Ray Fix   ############
    spell.caster.condition_add('Wf Ray Fix', 0)
############ Weapon Focus Ray Fix End ############

and be sure to have the python script in your overrides\scr folder.

Please be sure that if you use such fixes to mark them in your code, because if the bug gets fixed you need to be able to find it easily so you can remove it without too much troubles.

Fixed:
Righteous Fury Temp HP now expire properly when reduced to 0
Changed Summon Undead V to mode_target: from Location to Area (to match the other undead summons and to avoid spawning them on your head)
Diamondsteel now uses item_d20_query(Q_Armor_Get_AC_Bonus) which will result in a functional spell once next Temple+ version is live
Ghost Touch Armor now uses item_d20_query(Q_Armor_Get_AC_Bonus) which will result in a functional spell once next Temple+ version is live

Added spells: 
Visage of the Deity lesser
Lawful Sword 
Summon Undead IV
Castigate
Summon Undead V
Conviction
Foundation of Stone
Nightshield
Nimbus of Light
Brambles
Deific Warding
Frost Breath
Ghost Touch Armor (non functional)
Aid, Mass
Align Weapon Mass
Bless Weapon Swift
Anarchic Storm
Clutch of Orcus
Conviction, Mass
Corona of Cold
Demon Dirge
Devil Blight
Energy Vortex
Grace
Resist Energy Mass

Missing Spells
Bard 1: Inspirational Boost(1061), Joyful Noise(1060)
Bard 2: Whirling Blade (1083)
Assassin 3: Fangs of the Vampire King, Spider Poison(funnily not listed on dndtools, but its in the book.)
Bard 5: Bolts of Bedevilment(1104)
Pal 1: Grave Strike(1116), Rhino's Rush (1117), Lionheart, Divine Sacrifice
Pal 4: Draconic Might (Unsure how to do immunity), Sacred Haven
Clr 1: Light of Lunia
Clr 2: Light of Mercuria
Clr 3: Light of Venya

The Spell Compendium contains mass versions of spells that are in the PHB but not in ToEE:
Bless Weapon (has a constants.py entry = 039)
Align Weapon (no constants.py entry)