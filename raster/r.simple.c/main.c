
/****************************************************************************
 *
 * MODULE:       r.example.c
 * AUTHOR(S):    Markus Neteler - neteler itc.it
 *               with hints from: Glynn Clements - glynn gclements.plus.com
 * PURPOSE:      Just copies a raster map, preserving the raster map type
 *               Intended to explain GRASS raster programming
 *
 * COPYRIGHT:    (C) 2002, 2005-2009 by the GRASS Development Team
 *
 *               This program is free software under the GNU General Public
 *   	    	 License (>=v2). Read the file COPYING that comes with GRASS
 *   	    	 for details.
 *
 *****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <grass/gis.h>
#include <grass/raster.h>
#include <grass/glocale.h>

/*
 * global function declaration
 */
extern CELL f_c(CELL);
extern FCELL f_f(FCELL);
extern DCELL f_d(DCELL);

/*
 * function definitions
 */

CELL c_calc(CELL x)
{
    /* we do nothing exciting here */
    return x;
}

FCELL f_calc(FCELL x)
{
    /* we do nothing exciting here */
    return x;
}

DCELL d_calc(DCELL x)
{
    /* we do nothing exciting here */
    return x;
}

/*
 * main function
 * it copies raster input raster map, calling the appropriate function for each
 * data type (CELL, DCELL, FCELL)
 */
int main(int argc, char *argv[])
{
    char *name;			/* input raster name */
    char *result;		/* output raster name */
    struct GModule *module;	/* GRASS module for parsing arguments */
    struct Option *input, *output;	/* options */

    /* initialize GIS environment */
    G_gisinit(argv[0]);		/* reads grass env, stores program name to G_program_name() */

    /* initialize module */
    module = G_define_module();
    G_add_keyword(_("input"));
    G_add_keyword(_("output"));
    module->description = _("My first raster module");

    /* Define the different options as defined in gis.h */
    input = G_define_standard_option(G_OPT_R_INPUT);

    output = G_define_standard_option(G_OPT_R_OUTPUT);

    /* options and flags parser */
    if (G_parser(argc, argv))
	exit(EXIT_FAILURE);

    /* stores options and flags to variables */
    name = input->answer;
    result = output->answer;

    exit(EXIT_SUCCESS);
}
