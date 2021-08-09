from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Find the Gap"

def findTheGapSpellCheckTouchAttack(attachee, args, evt_obj):
    if args.get_arg(2): #only the first attack each round ignores armor
        return 0

    if not evt_obj.attack_packet.get_flags() & D20CAF_TOUCH_ATTACK:
        #evt_obj.attack_packet.set_flags(D20CAF_TOUCH_ATTACK) #does not work :(
        evt_obj.bonus_list.add_cap(9 , 0, 1, "~Find the Gap~[TAG_SPELLS_FIND_THE_GAP]")
        evt_obj.bonus_list.add_cap(10 , 0, 1, "~Find the Gap~[TAG_SPELLS_FIND_THE_GAP]")
        evt_obj.bonus_list.add_cap(28 , 0, 1, "~Find the Gap~[TAG_SPELLS_FIND_THE_GAP]")
        evt_obj.bonus_list.add_cap(29 , 0, 1, "~Find the Gap~[TAG_SPELLS_FIND_THE_GAP]")
        evt_obj.bonus_list.add_cap(33 , 0, 1, "~Find the Gap~[TAG_SPELLS_FIND_THE_GAP]")
        attachee.float_text_line("Find the Gap!")

    #Set Touch Attack Flag
    args.set_arg(2, 1)
    return 0

def findTheGapSpellResetFlag(attachee, args, evt_obj):
    args.set_arg(2, 0)
    return 0

findTheGapSpell = PythonModifier("sp-Find the Gap", 4) # spell_id, duration, notFirstAttack, empty
findTheGapSpell.AddHook(ET_OnGetAcModifierFromAttacker , EK_NONE, findTheGapSpellCheckTouchAttack,())
findTheGapSpell.AddHook(ET_OnBeginRound, EK_NONE, findTheGapSpellResetFlag, ())
findTheGapSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
findTheGapSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
findTheGapSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
findTheGapSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
findTheGapSpell.AddSpellDispelCheckStandard()
findTheGapSpell.AddSpellTeleportPrepareStandard()
findTheGapSpell.AddSpellTeleportReconnectStandard()
findTheGapSpell.AddSpellCountdownStandardHook()
