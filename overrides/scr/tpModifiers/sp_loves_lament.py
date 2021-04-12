from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Loves Lament"

def lovesLamentSpellPenalty(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-(args.get_arg(2)), 0, "~Loves Lament~[TAG_SPELLS_LOVES_LAMENT] Penalty") #Loves Lament penalty is passed by the spell
    return 0

def lovesLamentSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Loves Lament ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Loves Lament ({} rounds)".format(args.get_arg(1)))
    return 0

def lovesLamentSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("LOVES_LAMENT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("LOVES_LAMENT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def lovesLamentSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def lovesLamentSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def lovesLamentSpellSpellEnd(attachee, args, evt_obj):
    print "Loves Lament SpellEnd"
    return 0

lovesLamentSpell = PythonModifier("sp-Loves Lament", 3) # spell_id, duration, wisdomDamage
lovesLamentSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_WISDOM, lovesLamentSpellPenalty,())
lovesLamentSpell.AddHook(ET_OnGetTooltip, EK_NONE, lovesLamentSpellTooltip, ())
lovesLamentSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, lovesLamentSpellEffectTooltip, ())
lovesLamentSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, lovesLamentSpellSpellEnd, ())
lovesLamentSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, lovesLamentSpellHasSpellActive, ())
lovesLamentSpell.AddHook(ET_OnD20Signal, EK_S_Killed, lovesLamentSpellKilled, ())
lovesLamentSpell.AddSpellDispelCheckStandard()
lovesLamentSpell.AddSpellTeleportPrepareStandard()
lovesLamentSpell.AddSpellTeleportReconnectStandard()
lovesLamentSpell.AddSpellCountdownStandardHook()
