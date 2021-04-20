from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Devil Blight"

def demonDirgeSpellOnBeginRound(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellDamageDice = dice_new('1d6')
    spellDamageDice.number = 2
    game.create_history_freeform("{} is affected by ~Devil Blight~[TAG_SPELLS_DEVIL_BLIGHT]\n\n".format(attachee.description))
    attachee.float_text_line("Devil Blight", tf_red)
    game.particles('hit-HOLY-medium', attachee)
    attachee.spell_damage(spellPacket.caster, D20DT_MAGIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return 0

def devilBlightSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Devil Blight ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Devil Blight ({} rounds)".format(args.get_arg(1)))
    return 0

def devilBlightSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("DEVIL_BLIGHT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("DEVIL_BLIGHT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def devilBlightSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def devilBlightSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def devilBlightSpellSpellEnd(attachee, args, evt_obj):
    print "Devil Blight SpellEnd"
    return 0

devilBlightSpell = PythonModifier("sp-Devil Blight", 2) # spell_id, duration
devilBlightSpell.AddHook(ET_OnGetTooltip, EK_NONE, devilBlightSpellTooltip, ())
devilBlightSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, devilBlightSpellEffectTooltip, ())
devilBlightSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, devilBlightSpellSpellEnd, ())
devilBlightSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, devilBlightSpellHasSpellActive, ())
devilBlightSpell.AddHook(ET_OnD20Signal, EK_S_Killed, devilBlightSpellKilled, ())
devilBlightSpell.AddSpellDispelCheckStandard()
devilBlightSpell.AddSpellTeleportPrepareStandard()
devilBlightSpell.AddSpellTeleportReconnectStandard()
devilBlightSpell.AddSpellCountdownStandardHook()
