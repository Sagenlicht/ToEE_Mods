Spells are taken from the WotC Sourcebook Spell Compendium which itself is a collection of spells that WotC previously published in other sources, e.g. the Complete Adventurer Sourcebook.
Temple+ is needed!

Custom .mes filenames are all named spell_compendium_x.mes, partsys is spell_compendium_partsys.tab and protos.tab is spell_compendium_protos.tab
Uses customized history.mes and damage.mes, which are included so be careful. Both are not customizable.

finished = finished with maybe exceptions of cosmetics; WAT = Wrong Action (should be swift); functional = works but has minor functional errors; WIP = Work in Progress

ID      Spell Name                  SC Page Status      Comments
1050    Sound Lance                 196     merge0      but spell ignores Silence spell I belive
1051    Critical Strike              56     functional  spell_utils done
1052    Camouflage                   43     merge0      spell_utils done
1053    Appraising Touch             15     rejected    spell_utils done; new particles
1054    Phantom Threat              157     functional  check for ranged missing wonky; check for cannot be flanked missing (unsure if needed); spell_utils done
1055    Distort Speech               69     finished    spell_utils done, needs new particles
1056    Distract                     69     finished    spell_utils done
1057    Focusing Chant               96     merge0      spell_utils done, new particles
1058    Herald's Call               113     merge0      uses vanilla slow condition
1059    Improvisation               121     finished    spell_utils done, needs new particles and sound
1060    Joyful Noise                                    not yet started
1061    Inspirational Boost         124     functional
1062    Invisibility, Swift         125     merge0      uses Invisibility condition
1063    Ironguts                    126     finished    spell_utils done; uses nauseated as a secondary condition; deactivated nausea until finialized nauseated-condition
1064    Ironthunder Horn            126     merge0      add vanilla knockdown condition only
1065    Insidious Rhythm                    finished    spell_utils done, needs new particles
1066    Master's Touch              139     WIP         needs rework
1067    Serene Visage               182     merge0      spell_utils done
1068    Shock and Awe               189     finished
1069    Sticky Fingers              206     merge0      spell_utils done
1070    Undersong                   227     merge0      spell_utils done; new particles
1071    Distract Assailant           69     finished
1072    Insightfull Feint           124     functional  needs sound and different buff symbol; Unsure how to limit to feints, limited to combat atm
1073    Lightfoot                   132     finished
1074    Sniper's Shot               194     finished    spell_utils done; needs new particles?
1075    Sonic Weapon                195     finished
1076    Bonefiddle                   37     finished    spell_utils done; uses replaceCondition; needs new particles
1077    Cloud of Bewilderment        48     finished    uses nauseated condition
1078    Curse of Impending Blades    56     merge0      spell_utils done, new particles
1079    Wave of Grief               236     merge0      spell_utils done
1080    Harmonic Chorus             110     finished    needs new buff symbol + sound; dismiss missing
1081    Iron Silence                125     finished
1082    War Cry                     236     WAT         should be swift; uses panicked condition
1084    Bladeweave                   31     finished    Uses dazed condition
1085    Fell the Greatest Foe        90     finished
1086    Fire Shuriken                92     finished    Uses Protos ID 4998 (spell_compendium_protos.tab) 
1087    Phantom Foe                 156     functional  Threat check is not perfect
1088    Veil of Shadow              228     finished
1089    Curse of Imp. Blades, Mass   57     merge0      spell_utils done, uses single target version condition of spell; new particles
1090    Dissonant Chord              69     merge0
1091    Haunting Tune               110     finished
1092    Love's Lament               134     finished
1093    Ray of Dizziness            166     finished
1094    Wounding Whispers           242     finished
1095    Dirge of Discord             66     finished
1096    Allegro                       9     merge0      spell_utils done
1097    Find the Gap                 91     functional
1098    Wraithstrike                243     functional
1099    Resonating Bolt             174     finished
1100    Resistance, Greater         174     merge0      spell_utils done
1101    Fugue                       100     functional  DC40+ (attack an ally) disabled as it is not working
1102    Sirine's Grace              191     merge0      spell_utils done
1103    Dolorous Blow                70     finished
1104    Bolts of Bedevilment         37     WIP
1105    Cacophonic Burst             41     merge0
1106    Wail of Doom                233     finished
1107    Heart Ripper                111     finished
1108    Dirge                        65     finished
1109    Nixie's Grace               148     merge0      spell_utils done
1110    Ray of Light                167     merge0      uses existing blindness condition; uses wf_ray_fix
1111    Resistance, Superior        174     merge0      spell_utils done
1112    Strategic Charge            210     WAT
1113    Blessed Aim                  31     merge0
1114    Clear Mind                   47     finished
1115    Deafening Clang              59     WAT; WIP    does not deafen
1116    Grave Strike                107     needs cpp
1118    Faith Healing                87     merge0
1119    Summon Undead I             215     finished
1120    Angelskin                    11     merge0      spell_utils done
1121    Demonhide                    63     merge0      spell_utils done; new particles
1122    Summon Undead II            215     finished
1123    Hand of Divinity            109     finished    uses modified deity.mes
1124    Curse of Ill Fortune         56     merge0      spell_utils done
1125    Awaken Sin                   21     merge0
1126    Checkmates Light             46     finished
1127    Cloak of Bravery             47     finished
1128    Divine Protection            70     merge0      spell_utils done
1129    Quick March                 164     merge0      spell_utils done
1130    Shield of Warding           188     finished
1131    Blessing of Bahamut          31     merge0      spell_utils done
1132    Diamondsteel                        works with next temple version; finished
1133    Righteous Fury              177     finished
1134    Undead Bane Weapon          226     functional  is stacking with Weapon Bane; needs chain rework
1135    Weapon of the Deity         237     WIP
1136    Axiomatic Storm              22     finished
1137    Holy Storm                  115     finished
1138    Unholy Storm                227     finished
1139    Summon Undead III           215     finished
1140    Visage of the Deity, lesser 231     merge0      spell_utils done
1141    Lawful Sword                131     finished    needs chain rework
1142    Summon Undead IV            215     finished
1143    Castigate                    44     WIP         can hear missing
1144    Summon Undead V             215     finished
1145    Conviction                   52     merge0      spell_utils done
1146    Foundation of Stone          98     WIP         Needs check if own round
1147    Nightshield                 148     merge0      spell_utils done
1148    Nimbus of Light             148     finished
1149    Brambles                     38     finished
1150    Deific Vengeance             62     merge0      needs particles
1151    Frost Breath                100     merge0      uses sp-Daze
1152    Ghost Touch Armor           102     not working Uses 161 as Buff bonus type atm!
1153    Aid Mass                      8     finished    can't use original aid effect, due to changed max temp hp; spell_utils done;
1154    Align Weapon Mass             9     finished    Uses spell_radial_menu_options.mes
1155    Bless Weapon Swift           31     WAT
1156    Anarchic Storm               11     finished
1157    Clutch of Orcus              49     finished
1158    Conviction Mass              52     merge0
1159    Corona of Cold               52     finished
1160    align weapon                ---     not part of the spell_compendium
1161    Demon Dirge                  63     merge0      spell_utils done
1162    Devil Blight                 64     merge0      spell_utils done
1163    Energy Vortex                81     merge0      uses spell_radial_menu_options
1164    Grace                               finished
1165    Resist Energy Mass          174     merge0      uses resist elements condition
1166    Nauseating Breath           146     finished    uses nauseated-condition
1167    Slashing Darkness           191     merge0
1168    Spikes                      202     finished
1169    Tremor                      223     
1170    Weapon of Energy            236     
1171    Storm of Elemental Fury     


Temple+ Beta nightly 2674+ needed atm!

Bonus Types: 151 Alchemical; 153 Sacred; 154 Profane; 160 Storm effects; 161 Ghost Touch Armor Property (needs to be verified that this is not in the game already!)

Missing Spells
Bard 1: Joyful Noise(1060)
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

Unique Modifier ID's:
155 = Sirenes Grace
156 = Sticky Fingers
157 = Undersong
162 = Curse of Ill Fortune
163 = Curse of Impending Blades
164 = Wave of Grief