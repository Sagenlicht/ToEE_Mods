from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Curse of Impending Blades"

def curseOfImpendingBladesSpellPenaltyToAc(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-2, 0, "~Curse of Impending Blades~[TAG_SPELLS_CURSE_OF_IMPENDING_BLADES] penalty")
    return 0

def curseOfImpendingBladesSpellCheckRemoveBySpell(attachee, args, evt_obj): #not tested what happens if spell gets interrupted
    spellToCheck = tpdp.SpellPacket(evt_obj.data1)
    spellsThatRemoveCurse = [spell_break_enchantment, spell_remove_curse, spell_miracle, spell_wish]
    if spellToCheck.spell_enum in spellsThatRemoveCurse:
        args.condition_remove()
    return 0

def curseOfImpendingBladesSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Curse of Impending Blades (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append("Curse of Impending Blades (" + str(args.get_arg(1)) + " rounds)")
    return 0

def curseOfImpendingBladesSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("CURSE_OF_IMPENDING_BLADES"), -2, " (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append(tpdp.hash("CURSE_OF_IMPENDING_BLADES"), -2, " (" + str(args.get_arg(1)) + " rounds)")
    return 0

def curseOfImpendingBladesSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def curseOfImpendingBladesSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def curseOfImpendingBladesSpellSpellEnd(attachee, args, evt_obj):
    print "Curse of Impending BladesSpellEnd"
    return 0

curseOfImpendingBladesSpell = PythonModifier("sp-Curse of Impending Blades", 2) # spell_id, duration
curseOfImpendingBladesSpell.AddHook(ET_OnGetAC, EK_NONE, curseOfImpendingBladesSpellPenaltyToAc,())
curseOfImpendingBladesSpell.AddHook(ET_OnD20Signal, EK_S_Spell_Cast, curseOfImpendingBladesSpellCheckRemoveBySpell, ())
curseOfImpendingBladesSpell.AddHook(ET_OnGetTooltip, EK_NONE, curseOfImpendingBladesSpellTooltip, ())
curseOfImpendingBladesSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, curseOfImpendingBladesSpellEffectTooltip, ())
curseOfImpendingBladesSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, curseOfImpendingBladesSpellSpellEnd, ())
curseOfImpendingBladesSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, curseOfImpendingBladesSpellHasSpellActive, ())
curseOfImpendingBladesSpell.AddHook(ET_OnD20Signal, EK_S_Killed, curseOfImpendingBladesSpellKilled, ())
curseOfImpendingBladesSpell.AddSpellTeleportPrepareStandard()
curseOfImpendingBladesSpell.AddSpellTeleportReconnectStandard()
curseOfImpendingBladesSpell.AddSpellCountdownStandardHook()
