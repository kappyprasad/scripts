<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="1.0">

    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/workbook">
        <xsl:copy>
            <xsl:apply-templates/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="sheet">
        <xsl:variable name="name" select="@name"/>
        <xsl:element name="{$name}">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="row[@number > 0]">
        <xsl:copy>
            <xsl:for-each select="col">
                <xsl:variable name="number" select="@number"/>
                <xsl:variable name="name" select="../../row[@number = '0']/col[@number = $number]/text()"/>
                <xsl:element name="{$name}">
                    <xsl:value-of select="text()"/>
                </xsl:element>
            </xsl:for-each>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="*">
        <!-- swallow anything else -->
    </xsl:template>

</xsl:stylesheet>
