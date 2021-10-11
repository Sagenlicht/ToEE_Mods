from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Hand of Divinity"

def handOfDivinitySpellBonus(attachee, args, evt_obj):
    if args.get_arg(2): #Hand of Divinity is a +2 profane bouns to saves if deity is evil
        evt_obj.bonus_list.add(2, 154, "~Hand of Divinity~[TAG_SPELLS_HAND_OF_DIVINITY] ~Profane~[TAG_MODIFIER_PROFANE] Bonus")
    else: #Hand of Divinity is a +2 sacred bouns to saves if deity is non evil
        evt_obj.bonus_list.add(2, 153, "~Hand of Divinity~[TAG_SPELLS_HAND_OF_DIVINITY] ~Sacred~[TAG_MODIFIER_SACRED] Bonus")
    return 0

def handOfDivinitySpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Hand of Divinity ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Hand of Divinity ({} rounds)".format(args.get_arg(1)))
    return 0

def handOfDivinitySpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("HAND_OF_DIVINITY"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("HAND_OF_DIVINITY"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def handOfDivinitySpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def handOfDivinitySpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def handOfDivinitySpellSpellEnd(attachee, args, evt_obj):
    print "Hand of Divinity SpellEnd"
    return 0

handOfDivinitySpell = PythonModifier("sp-Hand of Divinity", 3) # spell_id, duration, isProfaneBonus
handOfDivinitySpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, handOfDivinitySpellBonus,())
handOfDivinitySpell.AddHook(ET_OnGetTooltip, EK_NONE, handOfDivinitySpellTooltip, ())
handOfDivinitySpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, handOfDivinitySpellEffectTooltip, ())
handOfDivinitySpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, handOfDivinitySpellSpellEnd, ())
handOfDivinitySpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, handOfDivinitySpellHasSpellActive, ())
handOfDivinitySpell.AddHook(ET_OnD20Signal, EK_S_Killed, handOfDivinitySpellKilled, ())
handOfDivinitySpell.AddSpellDispelCheckStandard()
handOfDivinitySpell.AddSpellTeleportPrepareStandard()
handOfDivinitySpell.AddSpellTeleportReconnectStandard()
handOfDivinitySpell.AddSpellCountdownStandardHook()
