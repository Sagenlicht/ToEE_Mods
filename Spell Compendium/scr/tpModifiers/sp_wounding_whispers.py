from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Wounding Whispers"

def woundingWhispersSpellDealDamage(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    attacker = evt_obj.attack_packet.attacker
    spellDamageDice = dice_new('1d6+' + str(spellPacket.caster_level))
    print spellDamageDice
    if attacker.distance_to(attachee) < 6: #Only melee & natural attacks are affected, reach weapons are save
        if not spellPacket.check_spell_resistance(attacker):
            attacker.float_text_line("Wounding Whispers", tf_red)
            attacker.spell_damage(attachee, D20DT_SONIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return 0

def woundingWhispersSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Wounding Whispers ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Wounding Whispers ({} rounds)".format(args.get_arg(1)))
    return 0

def woundingWhispersSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("WOUNDING_WHISPERS"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("WOUNDING_WHISPERS"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def woundingWhispersSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def woundingWhispersSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def woundingWhispersSpellSpellEnd(attachee, args, evt_obj):
    print "woundingWhispersSpellSpellEnd"
    return 0

woundingWhispersSpell = PythonModifier("sp-Wounding Whispers", 2) # spell_id, duration
woundingWhispersSpell.AddHook(ET_OnTakingDamage2, EK_NONE, woundingWhispersSpellDealDamage,())
woundingWhispersSpell.AddHook(ET_OnGetTooltip, EK_NONE, woundingWhispersSpellTooltip, ())
woundingWhispersSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, woundingWhispersSpellEffectTooltip, ())
woundingWhispersSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, woundingWhispersSpellSpellEnd, ())
woundingWhispersSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, woundingWhispersSpellHasSpellActive, ())
woundingWhispersSpell.AddHook(ET_OnD20Signal, EK_S_Killed, woundingWhispersSpellKilled, ())
woundingWhispersSpell.AddSpellDispelCheckStandard()
woundingWhispersSpell.AddSpellTeleportPrepareStandard()
woundingWhispersSpell.AddSpellTeleportReconnectStandard()
woundingWhispersSpell.AddSpellCountdownStandardHook()
