from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Fire Shuriken"

def fireShurikenSpellAutomaticallyProficient(attachee, args, evt_obj):
    weaponUsedForAttack = evt_obj.attack_packet.get_weapon_used()
    weaponUsedName= str(weaponUsedForAttack).split("(", 1)[0]
    if weaponUsedName == "Fire Shuriken":
        evt_obj.bonus_list.add(4,0,"~Fire Shurriken Proficiency~[TAG_SPELLS_FIRE_SHURIKEN] Proficiency Bonus")
    return 0

def fireShurikenSpellBeginRound(attachee, args, evt_obj):
    print "Fire Shuriken Proficiency Begin Round"
    stillHasFireShuriken = attachee.has_item(4998) #4998 is Protos.tab ID of Fire Shuriken
    if not stillHasFireShuriken:
        args.condition_remove()
    return 0

fireShurikenSpell = PythonModifier("sp-Fire Shuriken", 1) #not used
fireShurikenSpell.AddHook(ET_OnToHitBonus2, EK_NONE, fireShurikenSpellAutomaticallyProficient, ())
fireShurikenSpell.AddHook(ET_OnBeginRound, EK_NONE, fireShurikenSpellBeginRound, ())
