from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Cloak of Bravery"

def cloakOfBraverySpellOnConditionAdd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    radiusCloakOfBravery = (60.0 + (attachee.radius / 12.0))
    print "radiusCloakOfBravery :", radiusCloakOfBravery
    cloakOfBraveryId = attachee.object_event_append(OLC_CRITTERS, radiusCloakOfBravery)
    args.set_arg(3, cloakOfBraveryId)
    spellPacket.update_registry()
    attachee.condition_add_with_args('Cloak of Bravery Effect', args.get_arg(0), args.get_arg(1), args.get_arg(2), args.get_arg(3))
    return 0

def cloakOfBraverySpellOnEntered(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellCaster = spellPacket.caster
    spellTarget = evt_obj.target
    cloakOfBraveryId = args.get_arg(3)
    print "Cloak of Bravery enter: ",  spellTarget

    if cloakOfBraveryId != evt_obj.evt_id:
        print "ID Mismatch: Returned ID: {}, expected ID: {}".format(args.get_arg(3), evt_obj.evt_id)
        return 0

    if not spellTarget.is_friendly(spellCaster):
        print "Not a friendly target"
        return 0

    if spellPacket.add_target(spellTarget, 0):
        print "Added: ", spellTarget
        spellTarget.condition_add_with_args('Cloak of Bravery Effect', args.get_arg(0), args.get_arg(1), args.get_arg(2), args.get_arg(3))
    return 0


def cloakOfBraverySpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def cloakOfBraverySpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def cloakOfBraverySpellSpellEnd(attachee, args, evt_obj):
    print "Cloak of Bravery SpellEnd"
    return 0

cloakOfBraverySpell = PythonModifier("sp-Cloak of Bravery", 4) # spell_id, duration, spellBonus, eventId
cloakOfBraverySpell.AddHook(ET_OnConditionAdd, EK_NONE, cloakOfBraverySpellOnConditionAdd,())
cloakOfBraverySpell.AddHook(ET_OnObjectEvent, EK_OnEnterAoE, cloakOfBraverySpellOnEntered, ())
cloakOfBraverySpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, cloakOfBraverySpellSpellEnd, ())
cloakOfBraverySpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, cloakOfBraverySpellHasSpellActive, ())
cloakOfBraverySpell.AddHook(ET_OnD20Signal, EK_S_Killed, cloakOfBraverySpellKilled, ())
cloakOfBraverySpell.AddSpellDispelCheckStandard()
cloakOfBraverySpell.AddSpellTeleportPrepareStandard()
cloakOfBraverySpell.AddSpellTeleportReconnectStandard()
cloakOfBraverySpell.AddSpellCountdownStandardHook()
cloakOfBraverySpell.AddAoESpellEndStandardHook()

### Start Cloak of Bravery Effect ###

def cloakOfBraveryEffectSaveBonus(attachee, args, evt_obj):
    if evt_obj.flags & 0x100000: #d20_defs.h: D20STD_F_SPELL_DESCRIPTOR_FEAR = 21, // 0x100000
        evt_obj.bonus_list.add(args.get_arg(2), 13,"~Cloak of Bravery~[TAG_SPELLS_CLOAK_OF_BRAVERY] ~Morale~[TAG_MODIFIER_MORALE] Bonus") #13 = Morale; Bonus is passed from spell(arg3)
    return 0

def cloakOfBraveryEffectBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    return 0

def cloakOfBraveryEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Cloak of Bravery ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Cloak of Bravery ({} rounds)".format(args.get_arg(1)))
    return 0

def cloakOfBraveryEffectEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("CLOAK_OF_BRAVERY"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("CLOAK_OF_BRAVERY"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def cloakOfBraveryEffectSpellKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def cloakOfBraveryEffectOnLeaveAoE(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    cloakOfBraveryId = args.get_arg(3)
    if cloakOfBraveryId != evt_obj.evt_id:
        print "ID Mismach Cloak of Bravery"
        return 0
    args.condition_remove()
    return 0

def cloakOfBraveryEffectOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0

cloakOfBraveryEffect = PythonModifier("Cloak of Bravery Effect", 4) #spell_id, duration, spellBonus, eventId
cloakOfBraveryEffect.AddHook(ET_OnSaveThrowLevel, EK_NONE, cloakOfBraveryEffectSaveBonus, ())
cloakOfBraveryEffect.AddHook(ET_OnBeginRound, EK_NONE, cloakOfBraveryEffectBeginRound, ())
cloakOfBraveryEffect.AddHook(ET_OnGetTooltip, EK_NONE, cloakOfBraveryEffectTooltip, ())
cloakOfBraveryEffect.AddHook(ET_OnGetEffectTooltip, EK_NONE, cloakOfBraveryEffectEffectTooltip, ())
cloakOfBraveryEffect.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, cloakOfBraveryEffectOnLeaveAoE, ())
cloakOfBraveryEffect.AddHook(ET_OnConditionRemove, EK_NONE, cloakOfBraveryEffectOnRemove, ())

## End Cloak of Bravery Effect ###
