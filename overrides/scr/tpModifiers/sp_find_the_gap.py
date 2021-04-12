from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Find the Gap"

def findTheGapSpellAddTouchFlag(attachee, args, evt_obj):
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

    args.set_arg(2, 1) #set the flag
    return 0

def findTheGapSpellResetFlag(attachee, args, evt_obj):
    args.set_arg(2, 0)
    return 0

def findTheGapSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Find the Gap ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Find the Gap ({} rounds)".format(args.get_arg(1)))
    return 0

def findTheGapSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("FIND_THE_GAP"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("FIND_THE_GAP"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def findTheGapSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def findTheGapSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def findTheGapSpellSpellEnd(attachee, args, evt_obj):
    print "Find the Gap SpellEnd"
    return 0

findTheGapSpell = PythonModifier("sp-Find the Gap", 3) # spell_id, duration, notFirstAttack
findTheGapSpell.AddHook(ET_OnGetAcModifierFromAttacker , EK_NONE, findTheGapSpellAddTouchFlag,())
findTheGapSpell.AddHook(ET_OnBeginRound, EK_NONE, findTheGapSpellResetFlag, ())
findTheGapSpell.AddHook(ET_OnGetTooltip, EK_NONE, findTheGapSpellTooltip, ())
findTheGapSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, findTheGapSpellEffectTooltip, ())
findTheGapSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, findTheGapSpellSpellEnd, ())
findTheGapSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, findTheGapSpellHasSpellActive, ())
findTheGapSpell.AddHook(ET_OnD20Signal, EK_S_Killed, findTheGapSpellKilled, ())
findTheGapSpell.AddSpellDispelCheckStandard()
findTheGapSpell.AddSpellTeleportPrepareStandard()
findTheGapSpell.AddSpellTeleportReconnectStandard()
findTheGapSpell.AddSpellCountdownStandardHook()
